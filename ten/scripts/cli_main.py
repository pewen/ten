#!/usr/bin/python3

"""
Simple main to run TEN from cli

TODO:
----
* Por ahora, solo se puede simular usando forster. Modificar para que también
  acepte dexter.
"""

from __future__ import print_function, division
import argparse
import time
import sys

import numpy as np

sys.path.append('../../')

import ten
from ten.mechanisms import forster, dexter
from ten.utils.utils import read4file, generate_file_name
from ten.utils.write import write_header, write_body, \
    write_footer, write_seed_file


menssage = '\rCalculating with meanPath = {0}, traps = {1}, ' +\
           'r_traps = {2} and {3} aceptors ({4} of {5} experiments)\t'


def bi_expo(x, a1, b1, a2, b2):
    """
    Tri-exponential use to adjust the taus
    """
    return a1**2*np.exp(-x/b1**2) + a2**2*np.exp(-x/b2**2)


def bi_expo_norma(x, a1, b1, a2, b2, C):
    """
    Tri-exponential use to adjust the taus
    """
    return C*a1*np.exp(-x/b1) + C*a2*np.exp(-x/b2)


def main():
    # Read parameters from cli.
    parser = argparse.ArgumentParser(description='TEN')
    parser.add_argument('-c', '--config', dest='config',
                        default='experiment.conf',
                        help='path to configuration \
                        (initial parameters) file')
    parser.add_argument('-o', dest='out_path',
                        default='output/',
                        help='output path')
    args = parser.parse_args()

    # Initial menssage
    print("Starting TEN version: {0}\n".format(ten.__version__))

    # Read the configuration from file.
    print("Configuration file: {0}".format(args.config))
    init_param = read4file(args.config)

    # Total time
    time_all = time.time()

    # Create all the traps, aceptors and nanoparticles
    traps = ten.random.c_aceptors(init_param['traps'],
                                  init_param['traps_r_mechanisms'],
                                  init_param['traps_way'])
    aceptors = ten.random.c_aceptors(init_param['aceptors'],
                                     init_param['r_mechanisms'],
                                     init_param['way'])
    nanoparticles = ten.random.c_nanoparticles(init_param['r_mean'],
                                               init_param['tau_D'],
                                               init_param['mean_path'],
                                               init_param['epsilon'],
                                               traps)

    number_experiment = len(nanoparticles)
    actual_experiment = 0

    # Create the seed array
    if 'seed' not in init_param:
        init_param['seed'] = []
    if not init_param['seed']:
        seed = int(time.time())
        init_param['seed'] = [seed + 150*i for i in range(len(nanoparticles))]
    elif len(init_param['seed']) != len(nanoparticles):
        print('Generando las semillas')
        init_param['seed'] = [seed + 150*i for i in range(len(nanoparticles))]

    # Save the seed to seeds.conf file
    write_seed_file(init_param['seed'], args.out_path)

    for nanoparticle in nanoparticles:
        # Set the seed
        seed = init_param['seed'][actual_experiment]
        ten.random.set_seed(seed)

        # Generate an unique output file name.
        path_result, path_hist = generate_file_name(nanoparticle.mean_path,
                                                    nanoparticle.traps.number,
                                                    nanoparticle.traps.r_mechanisms,
                                                    args.out_path)

        write_header(path_result, nanoparticle,
                     init_param, actual_experiment)

        time_start = time.time()

        actual_experiment += 1
        for aceptor in aceptors:

            # Write menssage
            sys.stdout.write(menssage.format(nanoparticle.mean_path,
                                             nanoparticle.traps.number,
                                             nanoparticle.traps.r_mechanisms,
                                             aceptor.number,
                                             actual_experiment,
                                             number_experiment))

            out = ten.experiments.tricota(nanoparticle,
                                          aceptor,
                                          forster,
                                          init_param['exiton'],
                                          init_param['steps'],
                                          init_param['convergence'])

            write_body(path_result, path_hist, aceptor.number, out)

        total_time = time.time() - time_start
        write_footer(path_result, total_time)

    # End menssage
    print('\n\nTotal time:', (time.time() - time_all)/60, ' min')
    print("TEN finished succefully")


if __name__ == "__main__":
    main()
