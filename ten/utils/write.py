import platform
from datetime import datetime

import numpy as np


__all__ = ['write_header', 'write_body', 'write_adjust', 'write_footer']

# some used text formated
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

seed: {20}
seeds: {21}
"""


def write_header(path_result, nanoparticle, init_param, actual_experiment):
    """

    """
    with open(path_result, 'w') as result_f:

        # Write input parameters in the output file.
        output_header = text_input.format(datetime.now(),
                                          platform.platform(),
                                          platform.uname(),
                                          nanoparticle.r_param[0],
                                          nanoparticle.r_param[1],
                                          nanoparticle.tau_d,
                                          nanoparticle.mean_path,
                                          nanoparticle.epsilon,
                                          nanoparticle.traps.number,
                                          nanoparticle.traps.r_mechanisms,
                                          nanoparticle.traps.way,
                                          init_param['aceptors'],
                                          init_param['r_mechanisms'],
                                          init_param['way'],
                                          init_param['exiton'],
                                          init_param['r_electro'],
                                          init_param['experiments'],
                                          init_param['mechanisms'],
                                          init_param['steps'],
                                          init_param['convergence'],
                                          init_param['seed'][actual_experiment],
                                          init_param['seed'])
        result_f.write(output_header)

        # Write the nanoparticle configurations
        result_f.write('\n\n' + '-'*80 + '\n')
        result_f.write(str(nanoparticle) + '\n\n')
        result_f.write(result_header)


def write_body(path_result, path_hist, aceptor_number, out):
    """
    Write the result
    """
    with open(path_result, 'a') as result_f:
        result_f.write(result_format.format(aceptor_number,
                                            out[1],
                                            out[2], out[3],
                                            out[5], out[0],
                                            out[6], out[4],
                                            out[-1]))

    with open(path_hist, 'a') as hist_f:
        hist_f.write(histo_format.format(aceptor_number,
                                         str(out[-2])[1:-1]))


def write_adjust(path_result, init_param, adjust_results):
    with open(path_result, 'a') as result_f:
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


def write_footer(path_result, total_time):
    with open(path_result, 'a') as result_f:
        result_f.write('\nTotal time: {0} min\n\n'.format(total_time/60))
        result_f.write('TEN finished succefully')
