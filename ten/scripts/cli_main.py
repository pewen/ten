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
import platform
from datetime import datetime
import time
import sys
sys.path.append('../../')

import numpy as np
from scipy.optimize import curve_fit

import ten
from ten.mechanisms import forster, dexter
from ten.utils.utils import read4file, generate_file_name


def bi_expo(x, a1, b1, a2, b2):
    """
    Tri-exponential use to adjust the taus
    """
    return a1**2*np.exp(-x/b1) + a2**2*np.exp(-x/b2)


# some used text formated
menssage = '\rCalculating with {0} traps and {1} acceptors'
result_header = "Aceptores  TransfAceptores  TransfTrampas  " +\
                "TransfNaturales  Exitaciones  Eficiencia    " +\
                "LD(nm)\t PasosProm  Tiempo(minutos)\n\n"
result_format = "{0:9}\t {1:9}\t {2:8}\t {3:9}    {4:9}  " +\
                "{5:9.8f}  {6:9.5f}\t {7:9.5f}\t {8:7.3}\n"
histo_format = "{0}, {1}\n"
tau_head = "Ajuste de los decaimiento mediante la siguiente función " +\
           "(en cada ajuste las áreas estan normalizada)\n"
tau_head += "A1*exp(-t/b1) + A2*exp(-t/b2)\n\n"
tau_head += "Aceptores\t\t A1\t\tb1\t\tA2\t\tb2\t " +\
            "StandardDeviationErrors\n\n"
tau_format = "{0:9}\t {1:10.5f}\t {2:10.5f}\t {3:10.5f}\t " +\
             "{4:10.5f}\t" +\
             "{5:10.3f}\t {6:10.3f}\t {7:10.3f}\t {8:10.3f}\t\n"
text_input = """TEN {0}

{1}
{2}

Inputs parameters:
-----------------
NP radius mean: {3:.3f} nm
NP radius deviation: {4:.3f} nm
Tau_D: {5:.3f} ns
Mean free path: {6:.3f} nm
Epsilon: {7:.3f} nm

Traps numbers: {8}
Traps mechanisms radius: {9} nm
Traps way: {10}

Acceptors number: {11}
Aceptors mechanisms radius: {12} nm
Aceptors way: {13}

Exiton: {14}
Radius electro: {15}

Experiments: {16}
Mechanisms: {17}
Steps: {18}
convergence: {19}
"""


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

    time_all = time.time()

    # Variando el numero de trampas
    for traps_number in init_param['traps']:
        # creamos las trampas
        traps = ten.Aceptor(number=traps_number,
                            r_mechanisms=init_param['traps_r_mechanisms'],
                            way=init_param['traps_way'])
        # creamos la nanoparticula
        nanoparticle = ten.Nanoparticle([init_param['r_mean'],
                                         init_param['r_deviation']],
                                        init_param['tau_D'],
                                        init_param['mean_path'],
                                        init_param['epsilon'],
                                        traps)

        # Generate an unique output file name.
        path_result, path_hist = generate_file_name(init_param['mean_path'],
                                                    traps_number,
                                                    init_param['traps_r_mechanisms'], args.out_path)

        # open outputs files
        result_f = open(path_result, 'w')
        hist_f = open(path_hist, 'w')

        # Write input parameters in the output file.
        output_header = text_input.format(datetime.now(), platform.platform(),
                                          platform.uname(),
                                          init_param['r_mean'],
                                          init_param['r_desviation'],
                                          init_param['tau_D'],
                                          init_param['mean_path'],
                                          init_param['epsilon'],
                                          traps_number,
                                          init_param['traps_r_mechanisms'],
                                          init_param['traps_way'],
                                          init_param['aceptors'],
                                          init_param['r_mechanisms'],
                                          init_param['way'],
                                          init_param['exiton'],
                                          init_param['r_electro'],
                                          init_param['experiments'],
                                          init_param['mechanisms'],
                                          init_param['steps'],
                                          init_param['convergence'])
        result_f.write(output_header)

        time_start = time.time()

        # Write the nanoparticle configurations
        result_f.write('\n\n' + '-'*80 + '\n')
        result_f.write(str(nanoparticle) + '\n\n')
        result_f.write(result_header)

        adjust_results = []

        # variando el numero de aceptores
        for aceptor_num in init_param['aceptors']:
            # Write menssage
            sys.stdout.write(menssage.format(traps_number, aceptor_num))

            dopantes = ten.Aceptor(number=aceptor_num,
                                   r_mechanisms=init_param['r_mechanisms'],
                                   way=init_param['way'])

            out = ten.experiments.tricota(nanoparticle, dopantes,
                                          forster,
                                          init_param['exiton'],
                                          init_param['steps'],
                                          init_param['convergence'])

            # Ajuste de los taus
            n, bins = np.histogram(out[-2]*nanoparticle.delta_t,
                                   bins=max(out[-2]))
            popt, pcov = curve_fit(bi_expo, bins[:-1], n)

            # Factor de normalizacion
            factor = 1/(popt[0]**2*popt[1] + popt[2]**2*popt[3])
            popt[0] = popt[0]*factor
            popt[2] = popt[2]*factor

            adjust_results.append([popt, pcov])

            # write the result
            result_f.write(result_format.format(aceptor_num, out[1],
                                                out[2], out[3],
                                                out[5], out[0],
                                                out[6], out[4],
                                                out[-1]))
            hist_f.write(histo_format.format(aceptor_num,
                                             str(out[-2])[1:-1]))

        result_f.write('\n\n' + '-'*80 + '\n')

        # Guardo los tau en el archivo result
        result_f.write(tau_head)
        for num, aceptor_num in enumerate(init_param['aceptors']):
            perr = np.sqrt(np.diag(adjust_results[num][1]))
            # Los elevamos al cuadrado a A1 y A2 por calculamos los A1_prima
            result_f.write(tau_format.format(aceptor_num,
                                             adjust_results[num][0][0]**2,
                                             adjust_results[num][0][1],
                                             adjust_results[num][0][2]**2,
                                             adjust_results[num][0][3],
                                             perr[0], perr[1],
                                             perr[2], perr[3]))

        result_f.write('\n\n' + '-'*80 + '\n')

        end = time.time()
        result_f.write('\nTotal time: {0} min\n\n'.format((end - time_start)/60))
        result_f.write('TEN finished succefully')

        # close outputs files
        result_f.close()
        hist_f.close()

    # End menssage
    print('\n\nTotal time:', (time.time() - time_all)/60, ' min')
    print("TEN finished succefully")


if __name__ == "__main__":
    main()
