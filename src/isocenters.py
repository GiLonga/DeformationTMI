import numpy as np
from src.TMIgeometry import Patient
from sklearn.metrics import mean_squared_error

class IsoGeometry(Patient):
    def __init__(self, patient_instance:Patient, ):
        self.__dict__ = patient_instance.__dict__.copy()
        self.isocenters = None
        self.fields = None
        self.y=np.mean(self.mesh.vertices[self.find_max_ptv()][1])

    def find_max_ptv(self):
        """
        Find the 10th max points in term of z coordinate, usefult to set the field on the head.
        """
        z = self.mesh.vertices[:,2]
        top_10_head=np.argsort(z)[-10:]
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
        x=np.mean(self.mesh.vertices[self.N_keypoints[0]][0]+self.mesh.vertices[self.N_keypoints[1]][0])
        #y= np.mean(self.mesh.vertices[self.find_max_ptv(self.mesh)][1])
        z = np.mean(self.mesh.vertices[self.find_max_ptv()][2])

        return (x,self.y,z)

    def get_body_isocenters(self,):
        """
        Find the body isocenters from the keypoints
        """
        body_list = []
        return body_list
    
    def get_legs_isocenters(self,):
        """

        """
        return []
    
    def get_arms_isocenters(self,):
        """
        
        """
        return []
    
    def find_isocenters(self):
        """
        TO DO
        """
        iso_list=[]
        iso_list.append(self.get_head_isocenter())
        iso_list = iso_list + self.get_body_isocenters()
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