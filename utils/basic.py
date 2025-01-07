import trimesh
import os

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