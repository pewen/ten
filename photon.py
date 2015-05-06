import numpy as np

class Photon():
    def __init__(self, nanoparticle):
        """
        Create a photon object, whit a random position in the nanoparticle

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects
        
        """
        x = np.random.uniform(low=-nanoparticle.R, high=nanoparticle.R)
        y = np.random.uniform(low=-nanoparticle.R, high=nanoparticle.R)
        z = np.random.uniform(low=-nanoparticle.R, high=nanoparticle.R)
        self.photon = np.array([x, y, z])
            
    def walk(self):
        pass
    
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
