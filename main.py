from utils.basic import load_mesh
from utils.visual import plot_isocenters
from src.TMIgeometry import Patient
from src.isocenters import IsoGeometry
path = r"/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/RTPLAN004.dcm"

if __name__ == "__main__":

    template = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/template/high/PAT_TEMP_0.off")
    ptv0 = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/mesh_4.ply")
    
    temp_pat= Patient(template, Plan_path = "/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/RTPLAN001.dcm", template=True)
    pat = Patient(ptv0, path, )
    
    pat.set_p2p(temp_pat)
    pat.find_keypoints(temp_pat)

    pat0 = IsoGeometry (patient_instance = pat)
    pat0.find_isocenters(temp_pat.arms)

    plot_isocenters(pat.mesh, pat0.isocenters,)
    #plot_isocenters(pat.mesh, [pat.mesh.vertices[pat.N_keypoints[21]]], ) #TO CHECK PREDICTED KEYPOINTS
    #plot_isocenters(temp_pat.mesh, [temp_pat.mesh.vertices[temp_pat.keypoints[16]]], ) #TO CHECK ORIGINAL KEYPOINTS
    print(pat0.iso_rmse(temp_pat.arms))


    
    print("That's all folks!")
    