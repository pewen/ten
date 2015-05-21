"""
Probando
"""
import numpy as np
from math import e
from src.utils import generate_random_points_in_sphere

#Used to print the day in the output file
from datetime import datetime
#To save machine info
import platform
#to measure time
import time

class Exciton(object):
    def __init__(self, nanoparticle, num_exc, gen_exition):
        """
        A exciton, which will be inside the nanoparticle. It can be generated at any place of this, using the method laser_generated() or by using a chemical electrolysis electro_generated() method.

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects.
        num_exc : float
            Numbers of exitation of the same nanoparticle.
        gen_exition : str
            Way to generate the exiton
        """
        self.NP = nanoparticle
        self.num_exc = num_exc
        self.generation_exition = gen_exition

    def laser_generated(self):
        """
        Generate the random position of the exciton in any part of the nanoparticle, pretending that this is bombarded by a laser. Because the diameter of the nanoparticle is too small, it is assumed that all are bombarded with the same intensity.
        """
        point = generate_random_points_in_sphere(1, self.NP.R)
        self.position = point[0]

    def electro_generated(self):
        """
        This method is not yet implemented.
        
        The random position is generated by a chemical electrolysis. This position is generated between the radius R of the nanoparticle and a radius R - epsilon, where epsilon depends electrolysis.
        """
        pass
            
    def walk(self):
        """
        Exciton make a random walk inside the nanoparticle. Like in this case the radius is fixed (epsilon), the point of the random walk can generate using spherical coordinates. Then we'll have to check that taking this step, the exciton does not leave the nanoparticle 
        """
        a = 1
        new_R = np.zeros_like(self.position)
        while a == 1:
            theta = 2*np.pi*np.random.uniform()
            phi = np.arccos(2*np.random.uniform() - 1)
        
            new_R[0] = np.sin(phi)*np.cos(theta)*self.NP.epsilon
            new_R[1] = np.sin(phi)*np.sin(theta)*self.NP.epsilon
            new_R[2] = np.cos(phi)*self.NP.epsilon

            if sum((new_R + self.position)**2) <= self.NP.R*self.NP.R:
                a = 0

        self.position += new_R
    
    def P_ET(self):
        """
        Returns the sum of the probability that a exciton is transferred to the acceptor. Each probability has the form: (1 / tau_D) (R_0 / r [i]) ** 6 where r [i] is the distance between the exciton and each acceptor and R_0 Forster radius.

        Returns
        -------
        prob : float
             Probability that a exciton is transferred to the acceptor.
        """
        dist = np.zeros(self.NP.n_acceptors)
        for i in range(self.NP.n_acceptors):
            dist[i] = 1/sum((self.position - self.NP.acceptors_positions[i])**3)

        cte = self.NP.R_Forster**6/self.NP.tau_D
        prob = 1 - e**(self.NP.delta_t * cte*sum(dist))
        return prob

    def move(self):
        """
        We know what is the probability that the exciton is transferred to an acceptor or decay. We generate a random number and compare it with the probability of decay. If it is less, compared the same number with probability that is transferred.If less so, it does a random step and generate another random number until the exciton decay or transferred.
        """
        self.cant_decay = 0
        self.cant_transf = 0
        
        time_ini = time.time()
        
        for i in range(self.num_exc):
            a = 0
            num_walk = 0

            if self.NP.generation_acceptors == 'sup':
                self.NP.deposit_superficial_acceptors()
            else:
                self.NP.deposit_volumetrically_acceptors()

            if self.generation_exition == 'elec':
                self.electro_generated()
            else:
                self.laser_generated()
            
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
        Save the initial conditions, the output of the simulations, the aceptors positions and some information about the machine where you run the simulations to a file.
        In the list of TODO, we have to develop post-processing tools to plot the positions of the acceptor or the quenching eficiencicia. Moreover, with this information, we will be able to do a little profiling.
        
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
Epsilon: %.3f
Number of exitations: %.0f
""" %(datetime.now(), platform.platform(), platform.uname(), self.NP.R, self.NP.R_Forster, self.NP.L_D, self.NP.tau_D, self.NP.n_acceptors, self.NP.epsilon, self.num_exc)

        text_output ="""
Outputs:
--------
Delta_t: %.3f
Probability of decay: %.3f
Amount of decays: %.0f
Amount of transfers: %.0f
Quenching efficiency: %f

Total time in seg: %.3f""" %(self.NP.delta_t, self.NP.P_decay, self.cant_decay, self.cant_transf, self.efficiency, self.total_time)

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
