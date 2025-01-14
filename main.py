from utils.basic import load_mesh
from utils.visual import plot_isocenters, plot_geometry
from src.TMIgeometry import Patient
from src.isocenters import IsoGeometry
from data.process import Processing
import numpy as np
import os
import sys


Plane_path_S = os.path.join(os.path.dirname(__file__),"data/raw_data/RTPLAN002.dcm") #ToDo, save the paths in an external file 
index = 2

if __name__ == "__main__":

    print()


    process = Processing(20000)
    #process.process()
    normalized_paths = process.normalize_mesh()
    #process.shape_align(source_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/processed_data/Pat_Norm4.off", target_path= "/home/ubuntu/giorgio_longari/DeformationTMI/data/template/rem_PTV_Tot_new.off")

    template = load_mesh(os.path.join(os.path.dirname(__file__),"data/template/rem_PTV_Tot_new.off"))
    ptv0 = load_mesh(os.path.join(os.path.dirname(__file__),f"data/processed_data/processed_patient_{index}.off"))
    ptv0_or = load_mesh(os.path.join(os.path.dirname(__file__),f"data/raw_data/PAT_{index}.off"))
    
    temp_pat= Patient(template, template, Plan_path = os.path.join(os.path.dirname(__file__), "data/raw_data/RTPLAN001.dcm"), template=True)
    pat = Patient(ptv0, ptv0_or, Plane_path_S,)
    
    pat.set_p2p(temp_pat)
    pat.find_keypoints(temp_pat)

    pat0 = IsoGeometry (patient_instance = pat)
    T_pat = IsoGeometry (patient_instance = temp_pat)
    pat0.find_isocenters(temp_pat.arms)

    HR_temp = load_mesh(os.path.join(os.path.dirname(__file__),"data/template/high/PAT_TEMP_0.off"))
    
    pat0.find_fields()
    #plot_geometry(HR_temp.vertices, temp_pat.or_isocenters, temp_pat.or_fields, name = "Template")
    rmse = pat0.rmse(pat0.isocenters, pat0.fields, arms = temp_pat.arms)
    plot_geometry(process.vertexlist[index], pat0.isocenters, pat0.fields, rmse= rmse, name = f"PAT{index}")
    plot_geometry(process.vertexlist[index], pat0.or_isocenters, pat0.or_fields, rmse = [0.0,0.0], name = f"PAT{index}_GT")
   
    #plot_isocenters(HR_temp.vertices, temp_pat.or_isocenters, name = "Template")
    #plot_isocenters(process.vertexlist[index], reversed_isos, name = "GT", groundtruth_iso = pat0.or_isocenters)


    #plot_isocenters(pat.mesh, [pat.mesh.vertices[pat.N_keypoints[21]]], ) #TO CHECK PREDICTED KEYPOINTS
    #plot_isocenters(temp_pat.mesh, [temp_pat.mesh.vertices[temp_pat.keypoints[16]]], ) #TO CHECK ORIGINAL KEYPOINTS

    print("That's all folks!")
    