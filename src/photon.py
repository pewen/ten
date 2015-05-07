import numpy as np
from math import e

class Photon(object):
    def __init__(self, nanoparticle):
        """
        Create a photon, whith a random position inside the nanoparticle.
        Have to study more correctly way to generate points in spherical coordinates, to avoid if.

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects
        """
        self.NP = nanoparticle
        
        a = 1
        while a == 1:
            x = NP.random.uniform(low = -self.NP.R, high = self.NP.R)
            y = NP.random.uniform(low = -self.NP.R, high = self.NP.R)
            z = NP.random.uniform(low = -self.NP.R, high = self.NP.R)
            if x*x + y*y + z*z <= self.NP.R*self.NP.R:
                a = 0
        self.photon = np.array([x, y, z])
            
    def walk(self):
        """
        Photon make a random walk inside the nanoparticle. Like in this case the radius is fixed (epsilon), the point of the random walk can generate using spherical coordinates. Then we'll have to check that taking this step, the photon does not leave the nanoparticle 
        """
        a = 1
        new_R = np.zeros_like(self.photon)
        while a == 1:
            theta = 2*np.pi*np.random.uniform()
            phi = np.arccos(2*np.random.uniform - 1)
        
            new_R[0] = np.sin(phi)*np.cos(theta)*self.NP.epsilon
            new_R[1] = np.sin(phi)*np.sin(theta)*self.NP.epsilon
            new_R[2] = np.cos(phi)*self.NP.epsilon

            if sum((new_R + self.photon)**2) <= self.photon.R*self.photon.R:
                a = 0

        self.photon += new_R
    
    def P_ET(self):
        """
        Returns the sum of the probability that a photon is transferred to the acceptor. Each probability has the form: (1 / tau_D) (R_0 / r [i]) ** 6 where r [i] is the distance between the photon and each acceptor and R_0 Forster radius.

        Returns
        -------
        prob : float
             Probability that a photon is transferred to the acceptor.
        """
        dist = np.zeros(self.NP.n_acceptors)
        for i in range(self.NP.n_acceptors):
            dist[i] = (self.photon - self.NP.acceptors_positions[i])**3

        dist = 1/dist

        cte = self.NP.R_Forster**6/self.NP.tau_D
        prob = 1 - e**(self.np.delta_t * cte*sum(dist))

    def move(self):
        """

        """
        pass
