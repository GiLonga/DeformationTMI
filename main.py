from utils.basic import load_mesh
from utils.visual import plot_isocenters
from src.TMIgeometry import Patient
from src.isocenters import IsoGeometry
path = r"/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/RTPLAN004.dcm"

if __name__ == "__main__":

    template = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/template/rem_PTV_Tot_new.off")
    ptv0 = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/rem_PTV_Tot_4_new.off")
    
    temp_pat= Patient(template, template=True)
    pat = Patient(ptv0, path, )
    
    pat.set_p2p(temp_pat)
    pat.find_keypoints(temp_pat)

    pat0 = IsoGeometry (patient_instance = pat)
    print(pat0.find_max_ptv())
    print(pat0.find_isocenters())

    plot_isocenters(pat.mesh, pat0.isocenters, )
    print("OK")
    