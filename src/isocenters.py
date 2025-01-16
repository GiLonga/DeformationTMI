import numpy as np
from src.TMIgeometry import Patient
from sklearn.metrics import mean_squared_error
import warnings
warnings.simplefilter('always', UserWarning)
warnings.formatwarning = lambda message, category, filename, lineno, line=None: f'{message}\n'


class IsoGeometry(Patient):
    def __init__(self, patient_instance:Patient, ):
        self.__dict__ = patient_instance.__dict__.copy()
        self.isocenters = None
        self.fields = None
        self.y=np.mean(self.mesh_or.vertices[self.find_max_ptv()][:,1])

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
        x=(self.mesh_or.vertices[self.N_keypoints[10]][0]+self.mesh_or.vertices[self.N_keypoints[11]][0])/2
        #y= np.mean(self.mesh.vertices[self.find_max_ptv(self.mesh)][1])
        z = (self.mesh_or.vertices[self.N_keypoints[10]][2]+self.mesh_or.vertices[self.N_keypoints[11]][2])/2

        return (x,self.y,z)

    def get_body_isocenters(self, arms):
        """
        Find the body's isocenters from the keypoints
        """
        body_list = []

        if arms:
            x_shoulder = (self.mesh_or.vertices[self.N_keypoints[15]][0]+self.mesh_or.vertices[self.N_keypoints[16]][0])/2
            z_shoulder = (self.mesh_or.vertices[self.N_keypoints[17]][2])
            body_list.append((x_shoulder,self.y,z_shoulder))
        else:
            x_thorax = (self.mesh_or.vertices[self.N_keypoints[31]][0])
            z_thorax = (self.mesh_or.vertices[self.N_keypoints[31]][2])
            body_list.append((x_thorax,self.y,z_thorax))

            x_abd = (self.mesh_or.vertices[self.N_keypoints[32]][0])
            z_abd = (self.mesh_or.vertices[self.N_keypoints[32]][2])     
            body_list.append((x_abd,self.y,z_abd))       
            
        #TO CALCULATE THE x I  avereged the arms coordinates, TO BE REMOVED
        x_pelvis = (self.mesh_or.vertices[self.N_keypoints[18]][0]+(self.mesh_or.vertices[self.N_keypoints[20]][0]+self.mesh_or.vertices[self.N_keypoints[21]][0])/2)/2
        z_pelvis = (+self.mesh_or.vertices[self.N_keypoints[18]][2])


        
        body_list.append((x_pelvis,self.y,z_pelvis))


        return body_list
    
    
    def get_arms_isocenters(self,):
        """
        Find the arms' isocenters from the keypoints
        """
        arms_list = []
        arms_list.append(self.mesh_or.vertices[self.N_keypoints[20]])
        arms_list.append(self.mesh_or.vertices[self.N_keypoints[21]])
        return arms_list
    
    def get_legs_isocenters(self,):
        """
        Find the legs' isocenters from the keypoints
        """
        legs_list = []
        x_legs = self.mesh_or.vertices[self.N_keypoints[19]][0]
        z_legs = self.mesh_or.vertices[self.N_keypoints[19]][2] - 50
        legs_list.append((x_legs,self.y,z_legs))
        return legs_list
    
    
    def find_isocenters(self, arms):
        """
        TO DO
        """
        iso_list=[]
        iso_list.append(self.get_head_isocenter())
        iso_list = iso_list + self.get_body_isocenters(arms)
        if arms:
            iso_list = iso_list + self.get_arms_isocenters()
        iso_list = iso_list + self.get_legs_isocenters()
        self.isocenters = iso_list
        return self.isocenters
    
    def set_x_aperture(self, arms):
        """
        Set the x coordinate of the aperture
        """
        if arms == self.arms:
            field = (-200, 200)
        else:
            field = (-200, 200) #STUBBED
        return field

    def get_head_fields(self,):
        """
        Find the head fields from the keypoints
        """
        head_fields = []

        z_upper = np.mean(self.mesh_or.vertices[self.find_max_ptv()][:,2]) + 30
        head_iso = self.get_head_isocenter()
        z_up_aperture_1 = z_upper - head_iso[2]

        x_right = self.mesh_or.vertices[self.N_keypoints[10]][0]
        x_low_aperture_1 = x_right - head_iso[0] - 40

        x_left = self.mesh_or.vertices[self.N_keypoints[11]][0]
        x_low_aperture_2 = x_left - head_iso[0] + 40

        z_up_aperture_2, z_low_aperture_1 = self.hug_the_isocenter(head_iso)

        

        z_low = self.mesh_or.vertices[self.N_keypoints[25]][2]
        z_low_aperture_2 = z_low - head_iso[2]

        x_up_aperture_1 = x_right - head_iso[0] - 60
        x_up_aperture_2 = x_left - head_iso[0] + 60       

        head_fields.append((z_up_aperture_2, z_up_aperture_1,))
        head_fields.append((x_up_aperture_1, x_up_aperture_2,))
        head_fields.append((z_low_aperture_2, z_low_aperture_1))
        head_fields.append((x_low_aperture_1, x_low_aperture_2,))
        
        
        return head_fields
    
    def get_body_fields(self, arms):
        """
        Find the body fields from the keypoints
        """
        body_fields = []
        head_iso = self.get_head_isocenter()
        head_fields = self.get_head_fields()
        body_iso = self.get_body_isocenters(arms)
        arms_iso = self.get_arms_isocenters()

        z_shoulder_up_aperture_1, z_shoulder_low_aperture_1 = self.hug_the_isocenter(body_iso[0])
        z_shoulder_up_aperture_2 = head_iso[2] + head_fields[2][0] -body_iso[0][2]  + 30
        z_shoulder_low_aperture_2 = arms_iso[0][2] - body_iso[0][2] + 40

        body_fields.append((z_shoulder_up_aperture_1, z_shoulder_up_aperture_2,))
        body_fields.append((-200, 200))
        body_fields.append((z_shoulder_low_aperture_2, z_shoulder_low_aperture_1,))
        body_fields.append((-200, 200))

        z_pelvis_up_aperture_1, z_pelvis_low_aperture_1 = self.hug_the_isocenter(body_iso[1])
        z_pelvis_up_aperture_2 = body_iso[0][2] + z_shoulder_low_aperture_2 - body_iso[1][2] + 30
        z_pelvis_low_aperture_2 = -150 #STUBBED

        body_fields.append((z_pelvis_up_aperture_1, z_pelvis_up_aperture_2,))
        body_fields.append((-200, 200))
        body_fields.append((z_pelvis_low_aperture_2, z_pelvis_low_aperture_1,))
        body_fields.append((-200, 200))

        return body_fields
    
    def get_arms_fields(self,):
        """
        Find the arms fields from the keypoints
        """
        arms_fields = []
        arms_iso = self.get_arms_isocenters()
        x_arm_right_up = self.mesh_or.vertices[self.N_keypoints[27]][0] - arms_iso[0][0] -20
        x_arm_right_low = self.mesh_or.vertices[self.N_keypoints[28]][0] - arms_iso[0][0]
        x_arm_left_up = self.mesh_or.vertices[self.N_keypoints[30]][0] - arms_iso[1][0]
        x_arm_left_down = self.mesh_or.vertices[self.N_keypoints[29]][0] - arms_iso[1][0] +20

        arms_fields.append((x_arm_right_up, x_arm_right_low,))
        arms_fields.append((-200, 200))
        arms_fields.append((x_arm_left_up, x_arm_left_down,))
        arms_fields.append((-200, 200))
        
        return arms_fields
    
    def get_legs_fields(self, arms): 
        """
        Find the legs fields from the keypoints
        """
        legs_fields = []
        legs_iso = self.get_legs_isocenters()
        body_fields = self.get_body_fields(arms)
        body_iso = self.get_body_isocenters(arms)

        z_legs_up_aperture_1, z_legs_low_aperture_1 = self.hug_the_isocenter(legs_iso[0])
        z_legs_up_aperture_2 = body_iso[-1][2] + body_fields[-2][0] - legs_iso[0][2] + 50
        z_legs_low_aperture_2 = np.mean(self.mesh_or.vertices[self.find_min_ptv()][:,2]) - legs_iso[0][2] + 5

        legs_fields.append((z_legs_up_aperture_1, z_legs_up_aperture_2,))
        legs_fields.append((-200, 200))
        legs_fields.append((z_legs_low_aperture_2, z_legs_low_aperture_1,))
        legs_fields.append((-200, 200))

        return legs_fields
    
    def find_fields(self, arms):
        """
        Calculate the fields around the isocenters.
        """
        fields_list = []
        fields_list = fields_list + self.get_head_fields()
        fields_list = fields_list + self.get_body_fields(arms)
        if arms == True:
            fields_list = fields_list + self.get_arms_fields()
        fields_list = fields_list + self.get_legs_fields(arms)
        self.fields = fields_list
        return self.fields
    
    def hug_the_isocenter(self,isocenter):
        """
        Calculate the fields around the isocenter.
        """
        z_upper_field = -10
        z_lower_field = 10

        return z_upper_field, z_lower_field
    
    def iso_rmse(self, predicted ,arms, Two_Dim = True): #Can be switched between getter and setter
        """
        Calculate the rmse between the original isocenters and the predicted
        """
        if self.arms == arms:
            if Two_Dim:
                predicted = np.array(predicted)
                predicted = predicted[:,[0,2]]
                predicted = predicted.tolist()
                gt = np.array(self.or_isocenters)
                gt = gt[:,[0,2]]
                gt = gt.tolist()
                rmse = mean_squared_error(predicted, gt, squared=False)
            else:
                rmse = mean_squared_error(predicted, self.or_isocenters, squared=False)
            self.iso_RMSE = rmse
        else:
            rmse = mean_squared_error(predicted, self.or_isocenters[0], squared=False)
            self.iso_RMSE = rmse

        return  rmse
    
    def field_rmse(self, predicted, arms,):
        """
        Calculate the rmse between the original fields and the predicted
        """
        if self.arms == arms:
            rmse = mean_squared_error(predicted, self.or_fields, squared=False)
            self.field_RMSE = rmse
        return rmse
    
    def rmse(self, P_iso, P_fields, arms):
        """
        Calculate the rmse between the original patient geometry and the forcasted.
        """
        if self.isocenters == None or self.fields == None:
            ValueError("Before calculate the RMSE, calculate the isocenters and the fields")
        
        if len(self.isocenters) !=  len(self.or_isocenters):
            warnings.warn("\033[33m[DeformationTMI WARNING]\033[0m" + "Can't calculate the RMSE, the template and the patinet have a different geometry plan")
            return [38808,38808]

        rmse = []
        print("The total 2D RMSE is: ", self.iso_rmse(P_iso, arms, Two_Dim = True), "+", self.field_rmse(P_fields, arms), "=", self.iso_RMSE + self.field_RMSE)
        rmse.append(self.iso_RMSE + self.field_RMSE)

        print("The total 3D RMSE is: ", self.iso_rmse(P_iso, arms, Two_Dim = False), "+", self.field_rmse(P_fields, arms), "=", self.iso_RMSE + self.field_RMSE)
        rmse.append(self.iso_RMSE + self.field_RMSE)
        return rmse

    def rmse_REAL(self, P_iso, P_fields, arms):
        """
        Calculate the rmse between the original patient geometry and the forcasted.
        """
        if self.isocenters == None or self.fields == None:
            raise ValueError("Before calculate the RMSE, calculate the isocenters and the fields")
        
        if len(self.isocenters) !=  len(self.or_isocenters):

            warnings.warn("\033[33m[DeformationTMI WARNING]\033[0m" + "Can't calculate the RMSE, the template and the patinet have a different geometry plan")
            return [38808,38808]

        predicted = np.array(P_iso)
        predicted = predicted[:,[0,2]]
        predicted = predicted.tolist()
        gt = np.array(self.or_isocenters)
        gt = gt[:,[0,2]]
        gt = gt.tolist()

        RMSE_TOT_2D = mean_squared_error(predicted + P_fields , gt + self.or_fields, squared=False)

        print("The total 2D RMSE is: ", RMSE_TOT_2D)
        
        return RMSE_TOT_2D