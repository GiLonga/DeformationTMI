

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
    def init(self, PTV, template=False):
        self.mesh = PTV
        self.keypoints = self.set_keypoints()
        self.or_isocenters = self.load_isocenters()
        self.or_fields = self.load_fields()
        self.p2p=None
        self.template=template
        return
    
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
            None
        return keypoints
    
    def load_isocenters(self,):
        """
        This function set the real isocenters, ideally loading them from the dicom file.
        """
        return
    
    def load_fields(self,):
        """
        This function set the real fields, ideally loading them from the dicom file as aperture from the isocenter, and returns the coordinates in the space.
        NOTE: Is it the best choice? Maybe is better to calculate them as aperture? One coordinate to calculate, as it should be on a plane. To think about. 
        Maybe the isocenters are useful to be computed in the 3D domain, but of course not the fields.
        """
        return
    
    def load_p2p(self,):
        """
        Return the p2p calculated in the spectral section.
        """
        if self.template:
            ValueError("You can't calculate a point to point map for the Template. Check it!")

        return
    
    def calculate_keypoints(self,):
        """
        Calculate the keypoints exploiting the p2p.
        """

        if self.p2p == None:
            ValueError("Before calculate keypoints, set a p2p")

        return
    
    def find_ribs_border(self,):
        """
        Find the min point in term of z coordinate, usefult to set the field on the ribs.
        """
        return
    