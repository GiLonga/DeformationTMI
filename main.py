from utils.basic import load_mesh
from utils.visual import plot_isocenters, plot_geometry
from src.TMIgeometry import Patient
from src.isocenters import IsoGeometry
from data.process import Processing
import numpy as np

path = r"/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/RTPLAN002.dcm"
index = 2

if __name__ == "__main__":

    process = Processing(20000)
    #process.process()
    process.normalize_mesh()
    #process.shape_align(source_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/Pat_Norm4.off", target_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/template/rem_PTV_Tot_new.off")

    template = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/template/rem_PTV_Tot_new.off")
    ptv0 = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/processed_patient_2.off")
    
    temp_pat= Patient(template, Plan_path = "/home/ubuntu/giorgio_longari/DeformationTMI/data/raw_data/RTPLAN001.dcm", template=True)
    pat = Patient(ptv0, path,)
    
    pat.set_p2p(temp_pat)
    pat.find_keypoints(temp_pat)

    pat0 = IsoGeometry (patient_instance = pat)
    pat0.find_isocenters(temp_pat.arms)

    HR_temp = load_mesh("/home/ubuntu/giorgio_longari/DeformationTMI/data/template/high/PAT_TEMP_0.off")
    reversed_isos = (np.array(pat0.isocenters)+process.shiftlist[index])*process.alphalist[index]

    plot_geometry(HR_temp.vertices, temp_pat.or_isocenters, temp_pat.or_fields, name = "Template")
    #plot_isocenters(pat.mesh.vertices, pat0.isocenters, name = "Norm")
    #plot_isocenters(process.vertexlist[index], pat0.or_isocenters, name = "Original")
    #plot_isocenters(process.vertexlist[index], reversed_isos, name = "Real")
    #plot_isocenters(HR_temp.vertices, temp_pat.or_isocenters, name = "Template")
    #plot_isocenters(process.vertexlist[index], reversed_isos, name = "GT", groundtruth_iso = pat0.or_isocenters)


    #plot_isocenters(pat.mesh, [pat.mesh.vertices[pat.N_keypoints[21]]], ) #TO CHECK PREDICTED KEYPOINTS
    #plot_isocenters(temp_pat.mesh, [temp_pat.mesh.vertices[temp_pat.keypoints[16]]], ) #TO CHECK ORIGINAL KEYPOINTS
    #print(pat0.iso_rmse(reversed_isos[:], arms = temp_pat.arms))

    print("That's all folks!")
    