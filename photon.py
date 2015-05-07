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

            if (new_R + self.photon)**2 < self.photon.R*self.photon.R:
                a = 0

        self.photon += new_R
    
    def distance(self):
        """
        Return the array 'dist' where each component is the account 1/(r[i]**6), where r[i] is the distace bewteen the photon and each acceptors[i].
        """
        self.dist = np.zeros(self.np.n_acceptors)
        for i in range(self.np.n_acceptors):
            self.dist[i] = (sum((self.photon - self.np.acceptors_positions[i])**2))**3
