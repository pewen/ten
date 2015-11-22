#!/usr/bin/python3

from __future__ import print_function, division
import argparse
import sys

import numpy as np
from mpi4py import MPI

import ten

#######################################################################
# Read the init parameters
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config', dest='config',
                    default='experiment.conf',
                    help='path to configuration \
                    (initial parameters) file')
parser.add_argument('-o', dest='out_path',
                    default='output/',
                    help='output path')
parser.add_argument('-v', dest='verbose', action="store_true",
                    help='verbose')
args = parser.parse_args()

# Read the configuration from file.
init_param = ten.read4file(args.config)

# Inicialice some variables
output_parameters = []


#######################################################################
# Create a communicator
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


comm.Barrier()
t_start = MPI.Wtime()


#######################################################################
# Calculation of L_D
# using a radius which tends to infinity
if rank == 0:
    nano_particle = ten.NanoParticle(50000,
                                     0,
                                     0,
                                     init_param['tau_D'],
                                     init_param['R_Forster'],
                                     init_param['mean_path'],
                                     init_param['epsilon'],
                                     'vol')

    factor = int(10000/size)
    simu = ten.Exciton(nano_particle,
                       factor,
                       'laser')
    l_d = np.zeros(1)

else:
    simu = None
    l_d = None

simu = comm.bcast(simu, root=0)
l_d_local = simu.l_d()

comm.Reduce(l_d_local, l_d, op=MPI.SUM, root=0)

if rank == 0:
    l_d = l_d/size

comm.Barrier()


#######################################################################
# Calculation of Quenching efficiency
for num_acceptors in init_param['list_num_acceptors']:
    num_acceptors = int(num_acceptors)

    if rank == 0:
        # Initialice the nanopartile object,
        # depending the way to generate acceptors.
        if init_param['acceptors'] == 'sup':
            nano_particle = ten.NanoParticle(init_param['r_mean'],
                                             init_param['r_deviation'],
                                             num_acceptors,
                                             init_param['tau_D'],
                                             init_param['R_Forster'],
                                             init_param['mean_path'],
                                             init_param['epsilon'],
                                             'sup')
        elif init_param['acceptors'] == 'vol':
            nano_particle = ten.NanoParticle(init_param['r_mean'],
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

        factor = int(init_param['num_exc']/size)
        # Initialece the exiton,
        # depending the way to generate it's.
        if init_param['exiton'] == 'elec':
            simu = ten.Exciton(nano_particle,
                               factor,
                               init_param['r_elec'],
                               'elec')
        elif init_param['exiton'] == 'laser':
            simu = ten.Exciton(nano_particle,
                               factor,
                               'laser')
        else:
            print('Error: exiton must be laser or elec (have %s)'
                  %init_param['exiton'])
            sys.exit(-1)

        # To store the MPI.SUM of the local result
        result_reduce = np.zeros(5)

    else:
        # All processes must have a value for simu and result_reduce
        simu = None
        result_reduce = None

    # BroadCast of the `simu` object
    simu = comm.bcast(simu, root=0)

    # Calculing the efficiency
    simu.quenching()
    result_local = simu.get_output()

    comm.Reduce(result_local, result_reduce, op=MPI.SUM, root=0)

    if rank == 0:
        result_reduce[2:] = result_reduce[2:]/size
        output_parameters += [list(result_reduce)]


#######################################################################
# Save the output        
if rank == 0:
    input_parameters = simu.get_input()
    input_parameters.append(l_d)
    input_parameters[7] = int(input_parameters[7]*size)
    input_parameters.append(init_param['list_num_acceptors'])
    ten.save_out(input_parameters, output_parameters, args.out_path)


comm.Barrier()
t_diff = MPI.Wtime() - t_start
if args.verbose:
    if rank == 0:
        print('Total time: %.3f seg' %t_diff)
