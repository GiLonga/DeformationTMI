import os
import trimesh
import numpy as np
import sys
import re
import igl
import pandas as pd
from pathlib import Path
import pydicom
from skimage.draw import polygon
from skimage import measure

#from PyRMT import RMTMesh
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))
from utils.basic import sqrtarea, center_mass, translate
from utils.shape_transfer import shape_transfer


class Processing():
    """
    Class to process the data

    Parameters
    ------------
    Size: Number of points [int] to resize the mesh.
    """

    def __init__(self, remeshing_size):
        self.min_n_samples = remeshing_size
        self.vertexlist, self.faceslist, self.nameslist  = self.load_mesh()
        self.template_v, self.template_f, _ = self.load_mesh(os.path.join(os.path.dirname(__file__), "template/high"),)
        self.alphalist = []
        self.shiftlist = []
        self.path_to_norm = os.path.join(os.path.dirname(__file__), "processed_data")
        self.data_sheet = pd.read_excel(os.path.join(os.getcwd(), "data.xlsx"))

    def load_mesh(self, path= os.path.join(os.path.dirname(__file__), "raw_data") ) -> list:
        """Load the meshes from a folder.

        Parameters
        ----------
        Path : str
            Path to the folder that contains the files .off.

        Returns
        -------
        vertices : array-like, shape=[n_vertices, 3]
        faces : array_like, shape=[n_faces, 3]
        """    
        vetrex_list = []
        faces_list = []
        names_list = []
        file_names = os.listdir(path)
        sorted_file_names = sorted(file_names)
        try:
            for file_name in sorted_file_names:
                if file_name.lower().endswith('.off'):
                    full_path = os.path.join(path, file_name)
                    mesh = trimesh.load(full_path, process=True)
                    vetrex_list.append(mesh.vertices)
                    faces_list.append(mesh.faces)
                    names_list.append(file_name)

        except Exception as e:
            print(f"An error occurred: {e}")
        
        return vetrex_list,faces_list, names_list
    
    def remeshing(self,):
        """Hierarchical mesh from PyRMT.
        
        Based on [MBMR2023]_.

        References
        ----------
        .. [MBMR2023] Filippo Maggioli, Daniele Baieri, Simone Melzi, and Emanuele Rodolà.
            “ReMatching: Low-Resolution Representations for Scalable Shape
            Correspondence.” arXiv, October 30, 2023.
            https://doi.org/10.48550/arXiv.2305.09274.
        """
        for i,vertices,faces in enumerate(self.vertexlist, self.facelist):

            vetrex_list = []
            faces_list = []

            if not vertices.flags.f_contiguous:
                vertices = np.asfortranarray(vertices)

            if faces.dtype != np.int32:
                faces = faces.astype(np.int32)

            if not faces.flags.f_contiguous:
                faces = np.asfortranarray(faces)

            rhigh = RMTMesh(vertices, faces)
            rhigh.make_manifold()

            rlow = rhigh.remesh(self.min_n_samples)
            rlow.clean_up()

            vetrex_list.append(rlow.vertices)
            faces_list.append(rlow.triangles)

        return vetrex_list, faces_list
    
    def shape_align(self, source_path= "", target_path =os.path.join(os.path.dirname(__file__), "template/high/PAT_TEMP_0.off")):
        """Align the mesh to a Template.

        Parameters
        ----------
        source_path : str
            Path to the mesh to align.
        target_path : str 
            Path to the mesh Template.
        """   
        matches = re.findall(r'\d+', source_path)
        index = matches[-1] if matches else 0000
        path_aligned_mesh =shape_transfer(source_path, target_path, index)
        return 
    
    def normalize_mesh(self):
        """
        Normalize the area and shift the mesh.
        """
        path_list = []
        for i,(vertices,faces) in enumerate(zip(self.vertexlist, self.faceslist)):
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

            alpha = sqrtarea(mesh)
            mesh.vertices = vertices / alpha

            shift = center_mass(mesh)
            mesh = translate(mesh, -shift)

            self.alphalist.append(alpha)
            self.shiftlist.append(shift)
            path_list.append(os.path.join(self.path_to_norm, f"Norm{self.nameslist[i]}"))
            igl.write_triangle_mesh(path_list[i], mesh.vertices, faces)

        return path_list
    
    def reverse_normalize_mesh(self):
        """
        Reverse the normalization of the mesh.
        """
        for i,vertices,faces in enumerate(self.vertexlist, self.faceslist):
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            mesh.vertices = vertices * self.alphalist[i]
            self.vertexlist[i] = mesh.vertices
            igl.write_triangle_mesh(f"/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/processed_PAT_{i+4}.off", self.vertexlist[i], faces)
        return

    def process(self):
        """
        Pipeline to register the meshes to the target one.
        """   
        vl,fl = self.remeshing()
        for i,v,f in enumerate(vl,fl):
            self.shape_align(v, f, i)
        return
    
    def get_patien_param(self, index, ):
        """
        Function to get the patient parameters.
        """
        pat = self.data_sheet.iloc[index]

        pat_dict ={
                    "ID" : pat["PatientID"],
                    "arms" : pat["IsocenterOnArms"],
                    "x_dim" : pat["OrigMaskShape_x"],
                    "y_dim" : pat["OrigMaskShape_y"],
                    "z_dim" : pat["OrigMaskShape_z"],
                    "SliceThickness" : pat["SliceThickness"],
                    "PixelSpacing" : pat["PixelSpacing"],
                    "PTV_id" : pat["PTVID"]
                    }

        return pat_dict
    
    def world_to_voxel(self, coord, x_min, y_min, z_min, dx, dy, dz):
        """Convert real-world (x, y, z) coordinates to voxel indices"""
        i = int((coord[0] - x_min) / dx)
        j = int((coord[1] - y_min) / dy)
        k = int((coord[2] - z_min) / dz)
        return i, j, k
    
    def extract_ptv(self, idx: int,):

        PTV_number = None
        ex_data = self.data_sheet
        pat_dict = self.get_patien_param(idx, ex_data)

        dx = pat_dict["PixelSpacing"]
        dy = pat_dict["PixelSpacing"]
        dz = pat_dict["SliceThickness"]
        #voxel_size = (dx, dy, dz)
        local_dicom_path = Path(os.path.join(os.getcwd(), "dicom"))
        pat_folder = local_dicom_path / pat_dict["ID"]

        if not pat_folder.exists():
            raise FileNotFoundError(f"Patient folder not found: {pat_folder}")

        dicom_files = sorted(f for f in pat_folder.iterdir() if f.suffix.lower() == ".dcm")
        if len(dicom_files) != 2:
            raise FileNotFoundError(f"Expected 2 DICOM files (Plan & RT Struct), found {len(dicom_files)}.")
        plan_file, rt_struct_file = dicom_files

        plan = pydicom.dcmread(plan_file)
        rt_struct = pydicom.dcmread(rt_struct_file)

        contour_points = []
        for SetROI in rt_struct.StructureSetROISequence:
            if SetROI.ROIName.lower() in { pat_dict["PTV_id"].lower()}:
                PTV_number = SetROI.ROINumber
                break 
        if PTV_number is None:
            raise FileNotFoundError(f"I can't find a PTV for this Patient: {pat_dict['ID']}.")
        for roiCS in rt_struct.ROIContourSequence:
            if roiCS.ReferencedROINumber == PTV_number:
                roi = roiCS
                break
        for contour in roi.ContourSequence:
            points = np.array(contour.ContourData).reshape(-1, 3)
            contour_points.append(points)
        all_points = np.vstack(contour_points)
        x_min, x_max = min(all_points[:, 0]), max(all_points[:, 0])
        y_min, y_max = min(all_points[:, 1]), max(all_points[:, 1])
        z_min, z_max = min(all_points[:, 2]), max(all_points[:, 2])

        voxel_grid = np.zeros((pat_dict["x_dim"], pat_dict["y_dim"], pat_dict["z_dim"]), dtype=np.uint8)
        for contour in contour_points:
            z_voxel = self.world_to_voxel((0, 0, contour[0, 2]), x_min, y_min, z_min, dx, dy, dz)[2]

            x_voxels, y_voxels = [], []
            for point in contour:
                i, j, _ = self.world_to_voxel(point, x_min, y_min, z_min, dx, dy, dz)
                x_voxels.append(i)
                y_voxels.append(j)

            rr, cc = polygon(x_voxels, y_voxels, shape=voxel_grid.shape[:2])
            voxel_grid[rr, cc, z_voxel] = 1
            
        verts, faces = measure.marching_cubes(voxel_grid, level=0.5) # normals and values are not used
        verts_mm = np.zeros_like(verts)
        verts_mm[:, 0] = verts[:, 0] * dx + x_min  
        verts_mm[:, 1] = verts[:, 1] * dy + y_min  
        verts_mm[:, 2] = verts[:, 2] * dz + z_min 

        mesh_tri = trimesh.Trimesh(vertices=verts_mm, faces=faces)
        mesh_tri.export(f'raw_data/f{pat_dict["ID"]}.off', file_type='off')
        
if __name__ == "__main__":
    process = Processing(20000)
    #process.process()
    norm_path = process.normalize_mesh()
    #print(process.alphalist)
    process.shape_align(source_path= norm_path[0], target_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/template/rem_PTV_Tot_new.off")