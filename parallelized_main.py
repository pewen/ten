#!/usr/bin/python3

import numpy as np

from mpi4py import MPI

#Append to path to make the following imports
import sys
sys.path.append('../')

from src.nanoparticle import NanoParticle
from src.exciton import Exciton
from src.utils import read4file, save_out

import time

#To parse the argument from comand line
import argparse

# Creation of argument parser
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config',dest='config', default='./experiment.conf', help='path to configuration (initial parameters) file')
args = parser.parse_args()

# initial conditions
init_param = read4file(args.config)

#Inicialice some variables
input_parameters = []
output_parameters = []

for num_acceptors in np.linspace(init_param['num_acceptors_min'], init_param['num_acceptors_max'], init_param['num_simu']):
    num_acceptors = int(num_acceptors)

    #Create a communicator
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        #Create de nanopaticle
        nano_particle = NanoParticle(init_param['r'], num_acceptors, init_param['tau_D'], init_param['R_Forster'], init_param['L_D'], init_param['delta_t'], 'vol')

        #create the exiton
        factor = int(init_param['num_exc']/size)
        simu = Exciton(nano_particle, factor, 'laser')

        #Each process will save the results of the simulations in a unique position in the array.
        #That is, if we have N processes, the array will have N elements.
        sendbuf = np.zeros([size], dtype=np.int64)

    else:
        #All processes must have a value for sendbuf and nano_particle, but only the root process
        #is relevant. Here, all other processes have equal to None.
        simu = None
        sendbuf = None

    #Buffer to make the reduce (MPI.SUM) operations.
    reducebuf = np.zeros([1], dtype=np.int64)
    #Local array elemet to save the simulations results.
    sendbuf_local = np.zeros(1, dtype=np.int64)

    #BroadCast of the `simu` object
    simu = comm.bcast(simu, root=0)
    comm.Scatter(sendbuf, sendbuf_local, root=0)

    #  a = MPI.Wtick()
    #  b = MPI.Wtime()

    simu.move()

    sendbuf_local[0] = simu.cant_transf

    # print('From rank:', rank, 'cantidad de tranf es: ', sendbuf_local[0], 'wtime: ', MPI.Wtime() - b, 'tick: ', MPI.Wtick() - a)

    comm.Reduce(sendbuf_local, reducebuf, op=MPI.SUM, root=0)

    if rank == 0:
        input_parameters += [simu.get_input_parameters()]
        output_parameters += [simu.get_output()]

if rank == 0:
    save_out(input_parameters, output_parameters)