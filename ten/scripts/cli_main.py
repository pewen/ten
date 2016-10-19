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
from scipy.optimize import curve_fit
from scipy.integrate import quad

sys.path.append('../../')

import ten
from ten.mechanisms import forster, dexter
from ten.utils.utils import read4file, generate_file_name
from ten.utils.write import write_header, write_body, \
    write_adjust, write_footer


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

    # Set the seed
    if 'seed' not in init_param:
        init_param['seed'] = []
    if not init_param['seed']:
        seed = int(time.time())
        init_param['seed'] = [seed + 150*i for i in range(len(nanoparticles))]
    elif len(init_param['seed']) != len(nanoparticles):
        print('Generando las semillas')
        init_param['seed'] = [seed + 150*i for i in range(len(nanoparticles))]

    for nanoparticle in nanoparticles:

        seed = init_param['seed'][actual_experiment]
        ten.random.set_seed(seed)

        # Generate an unique output file name.
        path_result, path_hist = generate_file_name(nanoparticle.mean_path,
                                                    nanoparticle.traps.number,
                                                    nanoparticle.traps.r_mechanisms,
                                                    args.out_path)

        write_header(path_result, nanoparticle,
                     init_param, actual_experiment)

        adjust_results = []
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

            # Ajuste de los taus
            n, bins = np.histogram(out[-2]*nanoparticle.delta_t,
                                   bins=max(out[-2]))
            popt, pcov = curve_fit(bi_expo, bins[:-1], n, method="trf")

            # Factor de normalizacion
            popt = popt**2
            factor = 1/(popt[0]*popt[1] + popt[2]*popt[3])
            res, error = quad(bi_expo_norma, 0, np.inf,
                              args=(popt[0], popt[1], popt[2],
                                    popt[3], factor))

            popt[0] = popt[0]*factor
            popt[2] = popt[2]*factor

            adjust_results.append([popt, pcov])

            write_body(path_result, path_hist, aceptor.number, out)

        write_adjust(path_result, init_param, adjust_results)

        total_time = time.time() - time_start
        write_footer(path_result, total_time)

    # End menssage
    print('\n\nTotal time:', (time.time() - time_all)/60, ' min')
    print("TEN finished succefully")


if __name__ == "__main__":
    main()
