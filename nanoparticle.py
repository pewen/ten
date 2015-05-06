from scipy.constants import pi
import numpy as np
from math import cos, sin

class NanoParticle(object):
    def __init__(self, r, n_acceptors, tau_D, R_Forster):
        """
        Create a nanoparticle object
        
        Parameters
        ----------
        R : float
            Radio of nanoparticule
        n_acceptors : float
            Number of acceptors in the nanoparticle
        tau_D : float
            Lifetime of the donor
        R_Forster : float
            Radio de Forster
        """
        self.R = r
        self.n_acceptors = n_acceptors
        self.acceptors_positions = np.zeros((n_acceptors,3))
        self.tau_D = tau_D
        self.R_Forster = R_Forster
        
    def deposit_superficial_acceptors(self):
        """
        Generate random number of acceptors (n_acceptors) on the surface of the nanoparticle.
        """
        for i in range(self.n_acceptors):
            #Generate in spheric
            theta = np.random.uniform(low=0, high=2*pi)
            phi = np.random.uniform(low=0, high=pi)
            #Transform to cartesian
            self.acceptors_positions[i][0] = sin(phi)*cos(theta)*self.R
            self.acceptors_positions[i][1] = sin(phi)*sin(theta)*self.R
            self.acceptors_positions[i][2] = cos(phi)*self.R
    
    def deposit_volumetrically_acceptors(self):
        """
        Generate random number of acceptors (n_acceptors) anywhere in the nanoparticle.
        
        Is not easy generate random point usin spherical coordinates.
        For now, we generate random point in cartesian coordinates.
        Reference link to implement in sphereic: http://mathworld.wolfram.com/SpherePointPicking.html
        """
        for i in range(self.n_acceptors):
            self.acceptors_positions[i][0] = np.random.uniform(low=-self.R, high=self.R)
            self.acceptors_positions[i][1] = np.random.uniform(low=-self.R, high=self.R)
            self.acceptors_positions[i][2] = np.random.uniform(low=-self.R, high=self.R)
            
    def photon(self):
        """
        Generate random position of a photon in the nanoparticle.
        """
        x = np.random.uniform(low=-self.R, high=self.R)
        y = np.random.uniform(low=-self.R, high=self.R)
        z = np.random.uniform(low=-self.R, high=self.R)
        self.photon = np.array([x, y, z])
            
    def walk(self):
        pass
    
    def distance(self):
        """
        Calculate, for all acceptor, 1/(r**6), where r are the distace bewteen the photon and acceptors
        """
        self.dist = np.zeros(self.n_acceptors)
        for i in range(self.n_acceptors):
            self.dist[i] = (sum((self.photon - self.acceptors_positions[i])**2))**3
