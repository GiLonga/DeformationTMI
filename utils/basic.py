import trimesh
import os
from pyFM.mesh import geometry as geom
import numpy as np

def load_mesh(path="DeformationTMI/data/raw_data") -> list:
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
    if path == "DeformationTMI/data/raw_data" :  
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
    else: 
        mesh = trimesh.load(path, process=True)
    return mesh

def sqrtarea(mesh):
    """
    Square root of the area of a mesh.

    Parameters
    ----------
    mesh : trimesh.base.Trimesh
        mesh to compute the Area

    Returns
    -----------------
    sqrtarea : float
        square root of the area
    """
    if mesh.faces is None:
        return None
    faces_areas = geom.compute_faces_areas(mesh.vertices, mesh.faces)
    return np.sqrt(faces_areas.sum())

def vertex_areas(mesh):
    """
    per vertex area

    Returns
    -----------------
    vertex_areas : np.ndarray
        (n,) array of vertex areas
    """
    return geom.compute_vertex_areas(mesh.vertices, mesh.faces)

def center_mass(mesh):
    """
    center of mass

    Returns
    -----------------
    center_mass : np.ndarray
        (3,) array of the center of mass
    """
    return np.average(self.vertices, axis=0, weights=vertex_areas(mesh))