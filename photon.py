import numpy as np

class Photon():
    def __init__(self, nanoparticle):
        """
        Create a photon, whith a random position inside the nanoparticle.
        Have to study more correctly way to generate points in spherical coordinates, to avoid if.

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects
        """
        self.np = nanoparticle
        
        a = 1
        while a == 1:
            x = np.random.uniform(low = -self.np.R, high = self.np.R)
            y = np.random.uniform(low = -self.np.R, high = self.np.R)
            z = np.random.uniform(low = -self.np.R, high = self.np.R)
            if x*x + y*y + z*z < self.np.R*self.np.R:
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
        
            new_R[0] = np.sin(phi)*np.cos(theta)*self.np.epsilon
            new_R[1] = np.sin(phi)*np.sin(theta)*self.np.epsilon
            new_R[2] = np.cos(phi)*self.np.epsilon

            if (new_R + self.photon)**2 < self.photon.R:
                a = 0

        self.photon += new_R
    
    def distance(self, nanoparticle):
        """
        Calculate, for all acceptor, 1/(r**6), where r are the distace bewteen the photon and acceptors

        Parameters
        ----------
        nanoparticle : NanoParticle
        
        """
        self.dist = np.zeros(nanoparticle.n_acceptors)
        for i in range(nanoparticle.n_acceptors):
            self.dist[i] = (sum((self.photon - nanoparticle.acceptors_positions[i])**2))**3
