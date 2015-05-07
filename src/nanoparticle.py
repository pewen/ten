from scipy.constants import pi
import numpy as np
from math import cos, sin, e

class NanoParticle(object):
    def __init__(self, r, n_acceptors, tau_D, R_Forster, L_D, delta_t):
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
        L_D : float
            Length of exciton diffusion
        delta_t : float
            Time interval
        """
        #Nanoparticle parameters
        self.R = r
        self.n_acceptors = n_acceptors
        self.tau_D = tau_D
        self.R_Forster = R_Forster
        self.L_D = L_D
        self.delta_t = delta_t
        self.epsilon = L_D*delta_t/tau_D

        #decay probability
        self.P_decay = 1 - e**(-self.delta_t/self.tau_D)

        #Generate the acceptors positions array
        self.acceptors_positions = np.zeros((n_acceptors,3))
        
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
        
        Is not easy generate random point using spherical coordinates.
        For now, we generate random point in cartesian coordinates.
        Reference link to implement in sphereic: http://mathworld.wolfram.com/SpherePointPicking.html
        """
        for i in range(self.n_acceptors):
            self.acceptors_positions[i][0] = np.random.uniform(low=-self.R, high=self.R)
            self.acceptors_positions[i][1] = np.random.uniform(low=-self.R, high=self.R)
            self.acceptors_positions[i][2] = np.random.uniform(low=-self.R, high=self.R)

    def plot(self):
        """
        Plot, in a nice way and 3D, the nanoparticle and the acceptors.
        Each acceptor have a different color, depending the distance to the center of the nanoparticle.
        """
        pass
