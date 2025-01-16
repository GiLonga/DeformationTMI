from utils.basic import load_mesh
from utils.visual import plot_isocenters, plot_geometry
from src.TMIgeometry import Patient
from src.isocenters import IsoGeometry
from data.process import Processing
import numpy as np
import os
LOCAL_PATH = os.path.dirname(__file__)
pat_index = 4
Plane_path_S = os.path.join(LOCAL_PATH,f"data/raw_data/RTPLAN00{pat_index}.dcm") #ToDo, save the paths in an external file 
NORM_PAT = os.path.join(LOCAL_PATH,f"data/processed_data/NormPAT_{pat_index}.off")
DEF_PAT = os.path.join(LOCAL_PATH, "data/template/rem_PTV_Tot_new.off")

if __name__ == "__main__":

    process = Processing(20000)
    #process.process()
    normalized_paths = process.normalize_mesh()
    #process.shape_align(source_path= NORM_PAT, target_path = DEF_PAT )

    template = load_mesh(os.path.join(LOCAL_PATH,"data/template/rem_PTV_Tot_new.off"))
    ptv0 = load_mesh(os.path.join(LOCAL_PATH,f"data/processed_data/processed_patient_{pat_index}.off"))
    ptv0_or = load_mesh(os.path.join(LOCAL_PATH,f"data/raw_data/PAT_{pat_index}.off"))
    
    temp_pat= Patient(template, template, Plan_path = os.path.join(LOCAL_PATH, "data/raw_data/RTPLAN001.dcm"), template=True)
    pat = Patient(ptv0, ptv0_or, Plane_path_S,)
    
    pat.set_p2p(temp_pat)
    pat.find_keypoints(temp_pat)

    pat0 = IsoGeometry (patient_instance = pat)
    T_pat = IsoGeometry (patient_instance = temp_pat)
    pat0.find_isocenters(False)

    HR_temp = load_mesh(os.path.join(LOCAL_PATH,"data/template/high/PAT_TEMP_0.off"))
    
    
    plot_isocenters(process.vertexlist[pat_index-2], pat0.isocenters, name = f"PAT{pat_index}_isos")
    
    #WORKING ON THE FIELDS
 
    #pat0.find_fields(temp_pat.arms)
    #pat0.rmse_REAL(pat0.isocenters, pat0.fields, arms = temp_pat.arms)
    
    #CALCULATING THE RMSE
    #rmse = pat0.rmse(pat0.isocenters, pat0.fields, arms = temp_pat.arms)
    
    #PLOTTING THE GEOMETRY
    #plot_geometry(process.vertexlist[pat_index-2], pat0.isocenters, pat0.fields, rmse= rmse, name = f"PAT{pat_index}")
    #plot_geometry(process.vertexlist[pat_index-2], pat0.or_isocenters, pat0.or_fields, rmse = [0.0,0.0], name = f"PAT{pat_index}_GT")
    
    #OLD
    #plot_geometry(HR_temp.vertices, temp_pat.or_isocenters, temp_pat.or_fields, name = "Template")
    #plot_isocenters(HR_temp.vertices, temp_pat.or_isocenters, name = "Template")
    #plot_isocenters(process.vertexlist[pat_index], reversed_isos, name = "GT", groundtruth_iso = pat0.or_isocenters)

    #OLD
    #plot_isocenters(pat.mesh, [pat.mesh.vertices[pat.N_keypoints[21]]], ) #TO CHECK PREDICTED KEYPOINTS
    #plot_isocenters(temp_pat.mesh, [temp_pat.mesh.vertices[temp_pat.keypoints[16]]], ) #TO CHECK ORIGINAL KEYPOINTS

    print("That's all folks!")
    