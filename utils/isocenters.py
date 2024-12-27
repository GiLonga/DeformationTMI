import numpy as np
from src.TMIgeometry import Patient 
class Geometry(Patient):
    def init(self):
        self.isocenters = None
        self.fields = None

    def find_max_ptv(self):
        """
        Find the 10th max points in term of z coordinate, usefult to set the field on the head.
        """
        x, y, z = zip(self.mesh.vertices)
        top_10_head=np.argsort(z)[-10:]
        return top_10_head

    def find_min_ptv(self, ):
        """
        Find the 10th min points in term of z coordinate, usefult to set the field on the head.
        """
        x, y, z = zip(self.mesh.vertices)
        top_10_head=np.argsort(z)[:10]
        return top_10_head

    def get_head_isocenter(self, ):
        """
        Find the head isocenter from the keypoints
        """
        x=np.mean(self.mesh.vertices[self.keypoints[0]][0]+self.mesh.vertices[self.keypoints[1]][0])
        y= np.mean(self.mesh.vertices[self.find_max_ptv(self.mesh)][1])
        z = np.mean(self.mesh.vertices[self.find_max_ptv(self.mesh)][2])

        return (x,y,z)
    
    def find_isocenters(self):
        """
        TO DO
        """
        iso_list=[]
        iso_list.append(self.get_head_isocenter())

        self.isocenters = iso_list
        return
    
    def iso_rmse(self):
        """
        Calculate the rmse between the original isocenters and the predicted
        """
        return
    
    def field_rmse(self):
        """
        Calculate the rmse between the original fields and the predicted
        """
        return
    
    def rmse(self):
        """
        Calculate the rmse between the original patient geometry and the forcasted.
        """
        return self.iso_rmse() + self.field_rmse()