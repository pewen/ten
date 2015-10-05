"""
Excition Object
"""

import time
from math import e

import numpy as np

from src.utils import generate_random_points_in_sphere

class Exciton(object):
    def __init__(self, nanoparticle, num_exc, gen_exition, r_elec=0):
        """
        A exciton, which will be inside the nanoparticle.
        It can be generated at any place of this, with uniformal distribution,
        using the method laser_generated() or by using a chemical electrolysis
        electro_generated() method.

        Parameters
        ----------
        nanoparticle : object
            Nanoparticle objects.
        num_exc : float
            Numbers of exitation of the same nanoparticle.
        gen_exition : str
            Way to generate the exiton
        """
        self.nano_particle = nanoparticle
        self.num_exc = num_exc
        self.generation_exition = gen_exition
        self.r_electro = r_elec


    def laser_generated(self):
        """
        Generate the random position of the exciton in any
        part of the nanoparticle, pretending that this is
        bombarded by a laser. Because the diameter of the
        nanoparticle is too small, it is assumed that all
        are bombarded with the same intensity.
        """
        point = generate_random_points_in_sphere(1, self.nano_particle.radius)
        self.position = point[0]


    def electro_generated(self):
        """
        The random position is generated by a chemical electrolysis.
        This position is generated between the radius R of the
        nanoparticle and a radius r, where r depends electrolysis.
        """
        point = generate_random_points_in_sphere(1, self.nano_particle.radius,
                                                 self.r_electro)
        self.position = point[0]


    def walk(self):
        """
        Exciton make a random walk inside the nanoparticle.
        Like in this case the radius is fixed (epsilon),
        the point of the random walk can generate using spherical coordinates.
        Then we'll have to check that taking this step,
        the exciton does not leave the nanoparticle
        """
        check = 1

        while check == 1:
            new_r = generate_random_points_in_sphere(1, self.nano_particle.epsilon,
                                                     self.nano_particle.epsilon)[0]
            if sum((new_r + self.position)**2) <= self.nano_particle.radius*self.nano_particle.radius:
                check = 0

        self.position += new_r


    def p_transfer(self):
        """
        Returns the sum of the probability that a exciton is
        transferred to the acceptor. Each probability has the form:
        (1 / tau_D) (R_0 / r [i]) ** 6
        where r [i] is the distance between the exciton and
        each acceptor and R_0 Forster radius.

        Returns
        -------
        prob : float
             Probability that a exciton is transferred to the acceptor.
        """
        dist = np.zeros(self.nano_particle.n_acceptors)

        for i in range(self.nano_particle.n_acceptors):
            dist[i] = 1/sum((self.position -
                             self.nano_particle.acceptors_positions[i])**3)

        cte = self.nano_particle.r_forster**6/self.nano_particle.tau_d

        prob = 1 - e**(self.nano_particle.delta_t * cte*sum(dist))
        """
        for i in range(self.nano_particle.n_acceptors):
            dist[i] = 1/np.linalg.norm(self.position -
                                       self.nano_particle.acceptors_positions[i])

        sum_dist = sum(dist*dist*dist*dist*dist*dist)
        cte = self.nano_particle.r_forster**6/self.nano_particle.tau_d

        prob = 1 - e**(self.nano_particle.delta_t * cte*sum_dist)
        """

        return prob


    def calculate(self):
        """
        We know what is the probability that the exciton is transferred
        to an acceptor or decay. We generate a random number
        and compare it with the probability of decay.
        If it is less, compared the same number with probability
        that is transferred.If less so, it does a random step and
        generate another random number until the exciton decay or transferred.
        """

        self.cant_decay = 0
        self.cant_transf = 0
        num_walk = 0

        time_ini = time.time()
        self.positions_init = np.zeros((self.num_exc, 3))
        self.positions_end = np.zeros((self.num_exc, 3))

        for cont in range(self.num_exc):
            check = 0

            # Dopamiento
            if self.nano_particle.generation_acceptors == 'sup':
                self.nano_particle.deposit_superficial_acceptors()
            else:
                self.nano_particle.deposit_volumetrically_acceptors()

            # Excition
            if self.generation_exition == 'elec':
                self.electro_generated()
            else:
                self.laser_generated()

            self.positions_init[cont] = self.position

            while check == 0:
                rand_num = np.random.random()
                if self.nano_particle.p_decay > rand_num:
                    self.cant_decay += 1
                    check = 1
                elif self.p_transfer() > rand_num:
                    self.cant_transf += 1
                    check = 1
                else:
                    self.walk()
                    num_walk += 1

            self.positions_end[cont] = self.position

        dist = np.zeros(self.num_exc)
        resta = (self.positions_init - self.positions_end)**2

        dist[:] = np.sqrt(resta[:, 0] + resta[:, 1] + resta[:, 2])

        self.l_d_rms = np.sqrt(sum(dist**2)/len(dist))

        self.walk_mean = num_walk/self.num_exc
        self.total_time = time.time() - time_ini
        self.efficiency = self.cant_transf / self.num_exc


    def get_input(self):
        """Return a list with the imputs parametes"""
        return [self.nano_particle.radius, self.nano_particle.r_forster,
                self.nano_particle.l_d, self.nano_particle.tau_d,
                self.nano_particle.n_acceptors, self.nano_particle.epsilon,
                self.num_exc]


    def get_output(self):
        """Return a list with the output parameters"""
        return [self.nano_particle.delta_t, self.nano_particle.p_decay,
                self.cant_decay, self.cant_transf,
                self.efficiency, self.total_time,
                self.l_d_rms, self.walk_mean]

