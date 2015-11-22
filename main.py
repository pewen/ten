#!/usr/bin/python3

from __future__ import print_function, division
import argparse
import sys
import time

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

# Read the configuration from file
init_param = ten.read4file(args.config)

# Inicialice some variables
output_parameters = []

t_start = time.time()

#######################################################################
# Calculation of L_D
# using a radius which tends to infinity
nano_particle = ten.NanoParticle(50000,
                                 0,
                                 0,
                                 init_param['tau_D'],
                                 init_param['R_Forster'],
                                 init_param['mean_path'],
                                 init_param['epsilon'],
                                 'vol')

simu = ten.Exciton(nano_particle,
                   10000,
                   'laser')

l_d = simu.l_d()


#######################################################################
# Calculation of Quenching efficiency
for num_acceptors in init_param['list_num_acceptors']:
    num_acceptors = int(num_acceptors)

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

    # Initialece the exiton,
    # depending the way to generate it's.
    if init_param['exiton'] == 'elec':
        simu = ten.Exciton(nano_particle,
                           init_param['num_exc'],
                           init_param['r_elec'],
                           'elec')
    elif init_param['exiton'] == 'laser':
        simu = ten.Exciton(nano_particle,
                           init_param['num_exc'],
                           'laser')
    else:
        print('Error: exiton must be laser or elec (have %s)'
              %init_param['exiton'])
        sys.exit(-1)

    #Calculate
    simu.quenching()
    output_parameters += [list(simu.get_output())]


#######################################################################
# Save to file the output
input_parameters = simu.get_input()
input_parameters.append(l_d)    
input_parameters.append([x for x in init_param['list_num_acceptors']])

ten.save_out(input_parameters, output_parameters, args.out_path)


t_diff = time.time() - t_start
if args.verbose:
    print('Total time: %.3f seg' %t_diff)
