import numpy as np
from math import e

class Photon(object):
    def __init__(self, nanoparticle, num_exc):
        """
        Create a photon, whith a random position inside the nanoparticle.
        Have to study more correctly way to generate points in spherical coordinates, to avoid if.

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects
        num_exc : float
            Numbers of exitation of the same nanoparticle
        """
        self.NP = nanoparticle
        
        a = 1
        while a == 1:
            x = np.random.uniform(low = -self.NP.R, high = self.NP.R)
            y = np.random.uniform(low = -self.NP.R, high = self.NP.R)
            z = np.random.uniform(low = -self.NP.R, high = self.NP.R)
            if x*x + y*y + z*z <= self.NP.R*self.NP.R:
                a = 0
        self.photon = np.array([x, y, z])

        self.num_exc = num_exc
            
    def walk(self):
        """
        Photon make a random walk inside the nanoparticle. Like in this case the radius is fixed (epsilon), the point of the random walk can generate using spherical coordinates. Then we'll have to check that taking this step, the photon does not leave the nanoparticle 
        """
        a = 1
        new_R = np.zeros_like(self.photon)
        while a == 1:
            theta = 2*np.pi*np.random.uniform()
            phi = np.arccos(2*np.random.uniform() - 1)
        
            new_R[0] = np.sin(phi)*np.cos(theta)*self.NP.epsilon
            new_R[1] = np.sin(phi)*np.sin(theta)*self.NP.epsilon
            new_R[2] = np.cos(phi)*self.NP.epsilon

            if sum((new_R + self.photon)**2) <= self.NP.R*self.NP.R:
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
            dist[i] = 1/sum((self.photon - self.NP.acceptors_positions[i])**3)

        cte = self.NP.R_Forster**6/self.NP.tau_D
        prob = 1 - e**(self.NP.delta_t * cte*sum(dist))
        return prob

    def move(self):
        """
        
        """
        #number of random walks
        num_walk = 0

        a = 0
        
        #for i in range(self.num_exc):
        while a == 0:
            rand_num = np.random.random()
            if self.NP.P_decay > rand_num:
                print('Decae')
                a = 1
            elif self.P_ET() > rand_num:
                print('Se transfiere')
                a = 1
            else:
                self.walk()
                num_walk += 1

        print('Cantidad de pasos:', num_walk)
