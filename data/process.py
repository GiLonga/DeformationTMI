import os
import trimesh
import numpy as np
import sys
import re
import open3d as o3d
#from PyRMT import RMTMesh
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))
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
        self.vertexlist, self.faceslist  = self.load_mesh()
        self.template_v, self.template_f = self.load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/template/high")

    def load_mesh(self, path="DeformationTMI/data/raw_data") -> list:
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
        try:
            for file_name in os.listdir(path):
                if file_name.lower().endswith('.off'):
                    full_path = os.path.join(path, file_name)
                    mesh = trimesh.load(full_path, process=True)
                    vetrex_list.append(mesh.vertices)
                    faces_list.append(mesh.faces)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return vetrex_list,faces_list
    
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
    
    def shape_align(self, source_path= "", target_path ="/home/ubuntu/giorgio_longari/DeformationTMI/data/template/high/PAT_TEMP_0.off" ):
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
        shape_transfer(source_path, target_path, index)
        return
    
    def process(self):
        """
        Pipeline to register the meshes to the target one.
        """   
        vl,fl = self.remeshing()
        for i,v,f in enumerate(vl,fl):
            self.shape_align(v, f, i)
        return
    
if __name__ == "__main__":
    process = Processing(20000)
    #process.process()
    process.shape_align(source_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/PAT_4.off", target_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/template/high/PAT_TEMP_0.off")