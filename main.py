#!/usr/bin/python3

from __future__ import print_function, division
import argparse
import sys

from src.nanoparticle import NanoParticle
from src.exciton import Exciton
from src.utils import read4file, save_out

# Creation of argument parser
parser = argparse.ArgumentParser(description='TEN')
parser.add_argument('-c', '--config', dest='config',
                    default='experiment.conf',
                    help='path to configuration (initial parameters)\
                    file')
args = parser.parse_args()

# Read the configuration from file.
init_param = read4file(args.config)

# Inicialice some variables
output_parameters = []

for num_acceptors in range(init_param['num_acceptors_min'],
                           init_param['num_acceptors_max'],
                           init_param['acceptors_step']):
    num_acceptors = int(num_acceptors)

    # Initialice the nanopartile object,
    # depending the way to generate acceptors.
    if init_param['acceptors'] == 'sup':
        nano_particle = NanoParticle(init_param['r'],
                                     num_acceptors,
                                     init_param['tau_D'],
                                     init_param['R_Forster'],
                                     init_param['L_D'],
                                     init_param['epsilon'],
                                     'sup')
    elif init_param['acceptors'] == 'vol':
        nano_particle = NanoParticle(init_param['r'],
                                     num_acceptors,
                                     init_param['tau_D'],
                                     init_param['R_Forster'],
                                     init_param['L_D'],
                                     init_param['epsilon'],
                                     'vol')
    else:
        print('Error: acceptors must be vol o sup (have %s)'
              %init_param['acceptors'])
        sys.exit(-1)

    # Initialece the exiton,
    # depending the way to generate it's.
    if init_param['exiton'] == 'elec':
        simu = Exciton(nano_particle,
                       init_param['num_exc'],
                       init_param['r_elec'],
                       'elec')
    elif init_param['exiton'] == 'laser':
        simu = Exciton(nano_particle,
                       init_param['num_exc'],
                       'laser')
    else:
        print('Error: exiton must be laser or elec (have %s)'
              %init_param['exiton'])
        sys.exit(-1)

    #Calculate
    simu.quenching(each=init_param['each'])
    output_parameters += [simu.get_output()]

input_parameters = simu.get_input()
input_parameters.append([x for x in range(init_param['num_acceptors_min'],
                                          init_param['num_acceptors_max'],
                                          init_param['acceptors_step'])])

save_out(input_parameters, output_parameters)








