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
    def __init__(self, PTV, Plan_path="", template=False):
        self.mesh = PTV
        self.template=template
        self.PLAN_data = "" if template else pydicom.dcmread(Plan_path)
        self.keypoints = self.set_keypoints()
        self.or_isocenters = self.load_isocenters()
        self.or_fields = self.load_fields()
        self.p2p=None
        self.iso_RMSE=None
        self.field_RMSE=None
        self.arms = None
        self.N_keypoints = None

        
    
    def set_keypoints(self,):
        """
        A pre determinated set of keypoints, necessary to calculate the isocenters coordinates.
        """
        if self.template:
            keypoints = [ 9522, 11032, 10203, 10368,  9766,  9789, 10396, 10560, 10132, 9822, 5751, 15264, 10678, 10621, # maximum points head
              10397, #head low field
              1039, 19844, #shoulder's length
              10149, #second iso
              8529, #third iso
              8828, #fourth iso
              623, 19509, #iso on the arms
              3196, 16180, #heigth arm field
              5, #length arm field
              2972,  4055, 16249,  4330, 16175, 17162,  4532,  3627,  3625, 2971, #feet as minimum point of PTV
              ]
        else:
            keypoints=None
        return keypoints
    
    def load_isocenters(self,):
        """
        This function set the real isocenters, ideally loading them from the dicom file.
        """
        # Access the value at tag (300A, 012C)
        if self.template:
            return None
        isocenter_position = []
        tag = (0x300a, 0x00b0)
        if tag in self.PLAN_data:
            for beam in self.PLAN_data[tag]:
                new_iso = beam.ControlPointSequence[0].IsocenterPosition
                if new_iso not in isocenter_position:
                    isocenter_position.append(new_iso)

        if len(isocenter_position)==6:
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
        return
    
    def set_p2p(self, template):
        """
        Return the p2p calculated in the spectral section.
        """
        if self.template:
            ValueError("You can't calculate a point to point map for the Template. Check it!")

        p2p_21 = knn_query_normals(template.mesh.vertices, self.mesh.vertices,
                                        template.mesh.vertex_normals, self.mesh.vertex_normals,
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
    