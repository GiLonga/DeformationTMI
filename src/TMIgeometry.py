from utils.mapping import knn_query_normals 
import pydicom

class Patient():
    """Patient Class.

    Parameters
    ----------
    mesh : array-like, shape=[n_vertices, 3]
        Processed mesh of the patient.
    keypoints : array-like, shape=[N,3]
        Keypoints useful to obtain the isocenters.
    or_isocenters : array-like, shape=[M,3]
        Original isocenters in the plan.
    or_fields : array-like, shape=[M,3]
        Original fields in the plan.
    p2p : array-like, shape=[V]
        Point to point map between the template and the Patient
    template: Bool,
        To set as true if the instance is the template.
    """
    def __init__(self, PTV, PTV_or, Plan_path="", template=False):
        self.mesh = PTV
        self.mesh_or = PTV_or
        self.template=template
        self.arms = None
        self.p2p=None
        self.iso_RMSE=None
        self.field_RMSE=None
        self.N_keypoints = None
        self.PLAN_data = pydicom.dcmread(Plan_path)
        self.keypoints = self.set_keypoints()
        self.or_isocenters = self.load_isocenters()
        self.or_fields = self.load_fields()


        
    
    def set_keypoints(self,):
        """
        A pre determinated set of keypoints, necessary to calculate the isocenters coordinates.
        """
        if self.template:
            keypoints = [ 9522, 11032, 10203, 10368,  9766,  9789, 10396, 10560, 10132, 9822, 5751, 15264, 10678, 10621, # maximum points head
              10397, #head low field (index: 14)
              1039, 19844, #shoulder's length (index: 15-16)
              10154, #second iso (index: 17)
              8982, #third iso (index: 18)
              8828, #fourth iso (index: 19) 8828
              623, 19564, #iso on the arms (index: 20-21)
              3196, 16180, #heigth arm field (index: 22-23)
              5, #length arm field (index: 24)
              2004, 18857, # z head low field (index: 25-26)
              2, 1490, # x right arm field (index: 27-28)
              20263, 18700, # x left arm field (index: 29-30)
              10607, 10272, # second and third isos for standard patients (index: 31-32)
              ]
        else:
            keypoints=None
        return keypoints
    
    def load_isocenters(self,):
        """
        This function set the real isocenters, ideally loading them from the dicom file.
        """
        isocenter_position = []
        tag = (0x300a, 0x00b0)
        if tag in self.PLAN_data:
            for beam in self.PLAN_data[tag]:
                new_iso = beam.ControlPointSequence[0].IsocenterPosition
                if new_iso not in isocenter_position:
                    isocenter_position.append(new_iso)

        if len(isocenter_position) == 6:
            self.arms = True
        else:
            self.arms = False

        return isocenter_position
    
    def load_fields(self,):
        """
        This function set the real fields, ideally loading them from the dicom file as aperture from the isocenter, and returns the coordinates in the space.
        NOTE: Is it the best choice? Maybe is better to calculate them as aperture? One coordinate to calculate, as it should be on a plane. To think about. 
        Maybe the isocenters are useful to be computed in the 3D domain, but of course not the fields.
        """
        fields_aperture = []
        tag = (0x300a, 0x00b0)
        if tag in self.PLAN_data:
            for beam in self.PLAN_data[tag]:
                fields = beam.ControlPointSequence[0].BeamLimitingDevicePositionSequence
                z_fields = fields[0].LeafJawPositions
                x_fields = fields[1].LeafJawPositions
                fields_aperture.append(z_fields)
                fields_aperture.append(x_fields)
        return fields_aperture
    
    def set_p2p(self, template):
        """
        Return the p2p calculated in the spectral section.
        """
        if self.template:
            ValueError("You can't calculate a point to point map for the Template. Check it!")

        p2p_21 = knn_query_normals(self.mesh.vertices, template.mesh.vertices,
                                        self.mesh.vertex_normals, template.mesh.vertex_normals, 
                                        k_base=40, n_jobs=10) 
        self.p2p = p2p_21

        return
    
    def find_keypoints(self, template):
        """
        Calculate the keypoints exploiting the p2p.
        """

        if self.p2p is None:
            ValueError("Before calculate keypoints, set a p2p")
        if self.template:
            ValueError("Can't calculate the keypoints for the template")
        self.N_keypoints = self.p2p[template.keypoints]
        return self.N_keypoints

    def get_keypoints(self,):
        """
        Return the keypoints.
        """
        if self.keypoints == None:
            ValueError("Before get keypoints, calculate them with set_keypoints")
        return self.keypoints
    
    def find_ribs_edge(self,):
        """
        Find the min point in term of z coordinate, usefult to set the field on the ribs.
        """
        return
    