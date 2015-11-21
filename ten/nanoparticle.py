"""
NanoParticle Object
"""

from math import cos, sin, e, pi

import numpy as np

from .utils import generate_random_points_in_sphere

class NanoParticle(object):
    """Create a Nanoaprticle Object

    Methods:
    --------
    deposit_superficial_acceptors: no-arguments
      Acceptors are generated in the surface of the np
    deposit_volumetrically_acceptors: no-arguments
      Acceptors are generated volumetrically in the np

    """
    def __init__(self, r_mean, r_deviation,  num_acceptors, tau_D,
                 R_Forster, mean_path, epsilon, acceptors):
        """
        Create a nanoparticle object

        Parameters
        ----------
        r_mean : float
            Mean of the normal distribution nanoparticle radius. [r_mean] = nm.
        r_deviation : float, optional
            Standard deviation of the normal distribution nanoparticle radius.
            if not, the radius is considered constant. [r_deviation] = nm.
        n_acceptors : float
            Number of acceptors in the nanoparticle
        tau_D : float
            Lifetime of the donor. [tau_D] = ns.
        R_Forster : float
            Radio de Forster. [R_Forster] = nm.
        mean_path : float
            Length of mean free path. [mean_path] = nm.
        epsilon : float
            Step length on the random walk. [epsilon] = nm.
        acceptors : str
            Way to generate the acceptors. Can be 'sup' to generate
            on the surface or 'vol' to generate in all the nanoparticle.
        """
        # Nanoparticle parameters
        self.r_mean = r_mean
        self.r_deviation = r_deviation
        if r_deviation == 0:
            self.radius = r_mean
        else:
            self.radius = np.random.normal(r_mean, r_deviation)

        self.n_acceptors = num_acceptors
        self.tau_d = tau_D
        self.r_forster = R_Forster
        self.mean_path = mean_path
        self.delta_t = (epsilon*tau_D)/mean_path
        self.epsilon = epsilon
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
        points = generate_random_points_in_sphere(self.n_acceptors, self.radius, self.radius)
        self.acceptors_positions = points


    def deposit_volumetrically_acceptors(self):
        """
        Generate random position of n number acceptors (n_acceptors)
        uniformly distributed in the nanoparticle.
        """
        points = generate_random_points_in_sphere(self.n_acceptors, self.radius)
        self.acceptors_positions = points
