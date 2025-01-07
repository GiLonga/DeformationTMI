import numpy as np
from src.TMIgeometry import Patient
from sklearn.metrics import mean_squared_error

class IsoGeometry(Patient):
    def __init__(self, patient_instance:Patient, ):
        self.__dict__ = patient_instance.__dict__.copy()
        self.isocenters = None
        self.fields = None
        self.y=np.mean(self.mesh.vertices[self.find_max_ptv()][:,1])

    def find_max_ptv(self):
        """
        Find the 10th max points in term of z coordinate, usefult to set the field on the head.
        """
        z = self.mesh.vertices[:,2]
        top_10_head=np.argsort(z)[-15:]
        return top_10_head

    def find_min_ptv(self, ):
        """
        Find the 10th min points in term of z coordinate, usefult to set the field on the head.
        """
        z = self.mesh.vertices[:,2]
        bottom_10_legs=np.argsort(z)[:10]
        return bottom_10_legs

    def get_head_isocenter(self, ):
        """
        Find the head isocenter from the keypoints
        """
        x=(self.mesh.vertices[self.N_keypoints[10]][0]+self.mesh.vertices[self.N_keypoints[11]][0])/2
        #y= np.mean(self.mesh.vertices[self.find_max_ptv(self.mesh)][1])
        z = (self.mesh.vertices[self.N_keypoints[10]][2]+self.mesh.vertices[self.N_keypoints[11]][2])/2

        return (x,self.y,z)

    def get_body_isocenters(self,):
        """
        Find the body's isocenters from the keypoints
        """
        body_list = []
        x_shoulder = (self.mesh.vertices[self.N_keypoints[15]][0]+self.mesh.vertices[self.N_keypoints[16]][0])/2
        z_shoulder = (self.mesh.vertices[self.N_keypoints[15]][2]+self.mesh.vertices[self.N_keypoints[16]][2])/2
        body_list.append((x_shoulder,self.y,z_shoulder))

        x_pelvis = (self.mesh.vertices[self.N_keypoints[18]][0]+(self.mesh.vertices[self.N_keypoints[20]][0]+self.mesh.vertices[self.N_keypoints[21]][0])/2)/2
        z_pelvis = (self.mesh.vertices[self.N_keypoints[17]][2]+self.mesh.vertices[self.N_keypoints[18]][2])/2
        body_list.append((x_pelvis,self.y,z_pelvis))
        return body_list
    
    def get_arms_isocenters(self,):
        """
        Find the arms' isocenters from the keypoints
        """
        arms_list = []
        arms_list.append(self.mesh.vertices[self.N_keypoints[20]])
        arms_list.append(self.mesh.vertices[self.N_keypoints[21]])
        return arms_list
    
    def get_legs_isocenters(self,):
        """
        Find the legs' isocenters from the keypoints
        """
        legs_list = []
        legs_list.append(self.mesh.vertices[self.N_keypoints[19]])
        return legs_list
    
    
    def find_isocenters(self, arms):
        """
        TO DO
        """
        iso_list=[]
        iso_list.append(self.get_head_isocenter())
        iso_list = iso_list + self.get_body_isocenters()
        if arms:
            iso_list = iso_list + self.get_arms_isocenters()
        iso_list = iso_list + self.get_legs_isocenters()
        self.isocenters = iso_list
        return self.isocenters
    
    def iso_rmse(self): #Can be switched between getter and setter
        """
        Calculate the rmse between the original isocenters and the predicted
        """
        
        rmse = mean_squared_error(self.isocenters, self.or_isocenters, squared=False)
        self.iso_RMSE = rmse

        return  rmse
    
    def field_rmse(self):
        """
        Calculate the rmse between the original fields and the predicted
        """
        return
    
    def rmse(self):
        """
        Calculate the rmse between the original patient geometry and the forcasted.
        """
        print("The total RMSE is: ", self.iso_rmse() + self.field_rmse())
        return self.iso_RMSE + self.field_RMSE