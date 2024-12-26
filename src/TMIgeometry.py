

class Patient():
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
        return
    
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
        if self.template == True:
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
    