"""
NanoParticle Object
"""

from math import cos, sin, e, pi

import numpy as np

from src.utils import generate_random_points_in_sphere

class NanoParticle(object):
    def __init__(self, r, num_acceptors, tau_D, R_Forster, L_D,
                 delta_t, acceptors):
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
        acceptors : str
            Way to generate the acceptors
        """
        #Nanoparticle parameters
        self.radius = r
        self.n_acceptors = num_acceptors
        self.tau_d = tau_D
        self.r_forster = R_Forster
        self.l_d = L_D
        self.delta_t = delta_t
        self.epsilon = L_D*delta_t/tau_D
        self.generation_acceptors = acceptors

        #decay probability
        self.p_decay = 1 - e**(-self.delta_t/self.tau_d)

        #Generate the acceptors positions array
        self.acceptors_positions = np.zeros((self.n_acceptors, 3))


    def deposit_superficial_acceptors(self):
        """
        Generate random number of acceptors (n_acceptors)
        on the surface of the nanoparticle.
        """
        theta = 2*np.pi*np.random.uniform(size=self.n_acceptors)
        phi = np.arccos(2*np.random.uniform(size=self.n_acceptors) - 1)

        self.acceptors_positions[:, 0] = np.sin(phi)*np.cos(theta)*self.radius
        self.acceptors_positions[:, 1] = np.sin(phi)*np.sin(theta)*self.radius
        self.acceptors_positions[:, 2] = np.cos(phi)*self.radius


    def deposit_volumetrically_acceptors(self):
        """
        Generate random position of n number acceptors (n_acceptors)
        uniformly distributed in the nanoparticle.
        """
        points = generate_random_points_in_sphere(self.n_acceptors, self.radius)

        self.acceptors_positions = points
