import os
import trimesh
import numpy as np
from PyRMT import RMTMesh
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
    
    def shape_align(self, vertices, faces, index):
        """Align the mesh to a target.

        Parameters
        ----------
        vertices : numpy.array
            Array containing the vertices of a mesh.
        faces : numpy.array 
            Array containing the faces of a mesh.
        index : int
            key int to name the shape.
        """   
        target_shape = "PATH_TO_TARGET"
        shape_transfer(target_shape, vertices, faces, index)
    
    def process(self):
        """
        Pipeline to register the meshes to the target one.
        """   
        vl,fl = self.remeshing()
        for i,v,f in enumerate(vl,fl):
            self.shape_align(v, f, i)