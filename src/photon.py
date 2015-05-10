import numpy as np
from math import e

#Used to print the day in the output file
from datetime import datetime
#To save machine info
import platform
#to measure time
import time

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
        self.cant_decay = 0
        self.cant_transf = 0
        
        time_ini = time.time()
        
        for i in range(self.num_exc):
            a = 0
            num_walk = 0
            while a == 0:
                rand_num = np.random.random()
                if self.NP.P_decay > rand_num:
                    self.cant_decay += 1
                    a = 1
                elif self.P_ET() > rand_num:
                    self.cant_transf += 1
                    a = 1
                else:
                    self.walk()
                    num_walk += 1

        self.total_time = time.time() - time_ini
        self.efficiency = self.cant_transf / self.num_exc

    def save_out(self, file_path = '.', save_positions = True):
        """
        Save the output of the simulations to a file.
        Then, you can us 'Nombre del método' method to make the plot.
        Parameters
        ----------
        file_path : str, optional
            Path to save the file
        save_positions = boolean, optional
            If true, save the positions of aceptors in the output file
        """
        
        text_input = """TEN %s

%s
%s

Input parameters:
-----------------
NP radius: %.3f
Forster radius: %.3f
Length of excition diffusion: %.3f
Tau_D: %.3f
Number of acceptors: %.0f
Delta_t: %.3f
Epsilon: %.3f
Probability of decay: %.3f
Number of exitations: %.0f
""" %(datetime.now(), platform.platform(), platform.uname(), self.NP.R, self.NP.R_Forster, self.NP.L_D, self.NP.tau_D, self.NP.n_acceptors, self.NP.delta_t, self.NP.epsilon, self.NP.P_decay, self.num_exc)

        text_output ="""
Outputs:
--------
Amount of decays: %.0f
Amount of transfers: %.0f
Quenching efficiency: %f

Total time in seg: %.3f""" %(self.cant_decay, self.cant_transf, self.efficiency, self.total_time)

        if save_positions:

            #save the positions array of the aceptors in a string
            s = ''
            dim_y, dim_x = self.NP.acceptors_positions.shape
            for i in range(dim_y):
                for k in range(dim_x):
                    s += '%f\t' %(self.NP.acceptors_positions[i][k])
                s += '\n'
            
            text_positions = """
Aceptors positions(x, y, z):
%s""" %(s)
        
        f = open(file_path+'/tets.txt', 'a')
        f.write(text_input)
        if save_positions:
            f.write(text_positions)
        f.write(text_output)
        f.close()
