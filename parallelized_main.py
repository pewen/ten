#!/usr/bin/python3

from __future__ import print_function, division
import argparse
import sys

import numpy as np
from mpi4py import MPI

from src.nanoparticle import NanoParticle
from src.exciton import Exciton
from src.utils import read4file, save_out

# Creation of argument parser
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config', dest='config',
                    default='experiment.conf',
                    help='path to configuration (initial parameters)\
                    file')
parser.add_argument('-o', dest='out_path',
                    default='output/',
                    help='output path')
args = parser.parse_args()

# Read the configuration from file.
init_param = read4file(args.config)

# Inicialice some variables
output_parameters = []

for num_acceptors in range(init_param['num_acceptors_min'],
                           init_param['num_acceptors_max'],
                           init_param['acceptors_step']):
    num_acceptors = int(num_acceptors)

    # Create a communicator
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Initialice the nanopartile object,
        # depending the way to generate acceptors.
        if init_param['acceptors'] == 'sup':
            nano_particle = NanoParticle(init_param['r_mean'],
                                         init_param['r_deviation'],
                                         num_acceptors,
                                         init_param['tau_D'],
                                         init_param['R_Forster'],
                                         init_param['mean_path'],
                                         init_param['epsilon'],
                                         'sup')
        elif init_param['acceptors'] == 'vol':
            nano_particle = NanoParticle(init_param['r_mean'],
                                         init_param['r_deviation'],
                                         num_acceptors,
                                         init_param['tau_D'],
                                         init_param['R_Forster'],
                                         init_param['mean_path'],
                                         init_param['epsilon'],
                                         'vol')
        else:
            print('Error: acceptors must be vol o sup (have %s)'
                  %init_param['acceptors'])
            sys.exit(-1)

        # create the exiton
        factor = int(init_param['num_exc']/size)

        # Initialece the exiton,
        # depending the way to generate it's.
        if init_param['exiton'] == 'elec':
            simu = Exciton(nano_particle,
                           factor,
                           init_param['r_elec'],
                           'elec')
        elif init_param['exiton'] == 'laser':
            simu = Exciton(nano_particle,
                           factor,
                           'laser')
        else:
            print('Error: exiton must be laser or elec (have %s)'
                  %init_param['exiton'])
            sys.exit(-1)

        # Each process will save the results of the simulations in
        # a unique position in the array.
        # That is, if we have N processes, the array will have
        # N elements.
        sendbuf = np.zeros(size, dtype=np.int64)

    else:
        # All processes must have a value for sendbuf and
        # nano_particle, but only the root process
        # is relevant. Here, all other processes have equal to None.
        simu = None
        sendbuf = None

    # Buffer to make the reduce (MPI.SUM) operations.
    reducebuf = np.zeros(7)
    # Local array elemet to save the simulations results.
    sendbuf_local = np.zeros(7)

    # BroadCast of the `simu` object
    simu = comm.bcast(simu, root=0)
    #comm.Scatter(sendbuf, sendbuf_local, root=0)
    comm.Scatter(sendbuf, sendbuf_local, root=0)

    simu.quenching()

    sendbuf_local = simu.get_output()

    #print('Rank', rank, 'local bufer', sendbuf_local, '\n')

    comm.Reduce(sendbuf_local, reducebuf, op=MPI.SUM, root=0)

    if rank == 0:
        #print('reduce bufer', reducebuf, '\n')
        reducebuf[2:] = reducebuf[2:]/size
        output_parameters += [list(reducebuf)]
        #print('reduce bufer /2', reducebuf, '\n')
        #print('*'*100)

if rank == 0:
    input_parameters = simu.get_input()
    input_parameters[7] = int(input_parameters[7]*size)
    input_parameters.append([x for x in range(init_param['num_acceptors_min'],
                                              init_param['num_acceptors_max'],
                                              init_param['acceptors_step'])])
    save_out(input_parameters, output_parameters, args.out_path)
