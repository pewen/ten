"""
Functions that appears frequently in code
"""

from __future__ import division, absolute_import, print_function
from datetime import datetime
import platform
import sys
import os


def scrapyline(dic, keys, line):
    # Split the text and the value
    text, val = line.split(sep='=')
    # Sacamos las dobles comillas si las hay
    if "'" in val:
        val = val.replace("'", '')
    elif '"' in val:
        val = val.replace('"', '')
    # Si es una lista, la agarramos como tal
    if "[" in val:
        val = val[1:-1].split(',')
    # Intentar combirtirlos es float (cuando sea posible)
    try:
        val = float(val)
    except:
        pass
    for key in keys:
        if text == key:
            dic[key] = val


def read4file(file_path):
    """
    Read the initial parameter for a file.
    The file can have multiple lines of comments, always, starting
    with "" "and end with" "".
    The symbol # is considered line comment.

    Parameters
    ----------
    file_path : str
        Path to the file
    """
    keys = ['r_mean', 'r_desviation', 'tau_D', 'mean_path', 'epsilon',
            'traps', 'traps_r_mechanisms', 'traps_way',
            'aceptors', 'r_mechanisms', 'way',
            'exiton', 'r_electro',
            'experiments', 'mechanisms', 'excitations', 'steps', 'convergence']
    experiment_file = open(file_path, 'r')

    init_param = {}

    while True:
        a = experiment_file.readline()

        # Salteo todo los comentarios que usan """
        if '"""' in a:
            while True:
                a = experiment_file.readline()
                if '"""' in a:
                    a = experiment_file.readline()
                    break

        # Salteo todo los comentarios que usan '''
        elif "'''" in a:
            while True:
                a = experiment_file.readline()
                if "'''" in a:
                    a = experiment_file.readline()
                    break

        if a == '\n':
            continue

        # End of file
        if a == '':
            break

        if a.startswith('#'):
            continue

        # Remove all comment with "#"
        if '#' in a:
            a, rest = a.split('#')

        # Remove all spaces
        a = ''.join(a.split())

        scrapyline(init_param, keys, a)
    experiment_file.close()

    if init_param['exiton'] == 'elec' and 'r_electro' not in init_param:
        print('Error: If you generate the exiton by electrolysis,\
              you have to give a value of r_electro')
        sys.exit(-1)

    if 'r_deviation' not in init_param:
        init_param['r_deviation'] = 0

    init_param['traps'] = [int(i) for i in init_param['traps']]
    init_param['aceptors'] = [int(i) for i in init_param['aceptors']]

    return init_param


def generate_file_name(path='.'):
    results_files = [i for i in os.listdir(path) if i.startswith('result')]

    if not results_files:
        file_name = 'result.dat', 'hist.dat'
        return file_name

    max_num = 0
    for result_file in results_files:
        text, ext = result_file.split('.')
        a, num = text.split('result')
        if num == '':
            max_num = 0
        else:
            num = int(num)
            if num > max_num:
                max_num = num

    file_name = ('result{0}.dat'.format(max_num + 1),
                 'hist{0}.dat'.format(max_num + 1))
    return file_name


def save_out(input_parameters, output_parameters,
             time, file_path='output/'):
    """
    Save the output in a file.

    In the list of TODO, we have to develop post-processing tools
    to plot the positions of the acceptor or the quenching eficiencicia.
    Moreover, with this information, we will be able to do a little profiling.
    """
    cant_decay = extrac_from_list(output_parameters, 0)
    cant_transf = extrac_from_list(output_parameters, 1)
    efficiency = extrac_from_list(output_parameters, 2)
    total_time = extrac_from_list(output_parameters, 3)
    walk_mean = extrac_from_list(output_parameters, 4)
    acceptors = input_parameters[11]
    num_process = input_parameters[12]
    ld_calculate = input_parameters[10]

    if num_process == 'serial':
        process_text = "with serial code"
    else:
        process_text = " with %.0f process"%num_process

    text_input = """TEN {0}

{1}
{2}

Input parameters:
-----------------
NP radius mean: {3:.3f} nm
NP radius deviation: {4:.3f} nm
Foster radius: {5:.3f} nm
Mean free path: {6:.3f} nm
Tau_D: {7:.3f} ns
Number of acceptors: {8}
Epsilon: {9:.3f} nm
Number of exitations: {10:.0f}
Delta_t: {11:.3f} ns

Output parameters:
------------------
L_D = {12} nm
Probability of decay: {13}
Total time = {14:4.3f} seg {15}

""".format(datetime.now(), platform.platform(), platform.uname(),
           input_parameters[0], input_parameters[1], input_parameters[2],
           input_parameters[3], input_parameters[4], acceptors,
           input_parameters[6], input_parameters[7], input_parameters[8],
           ld_calculate, input_parameters[9], time, process_text)


    table_head = "| Nº acceptors | Amount of decays | Amount of transfers | Quenching efficiency | Step's Walk mean | Total time [seg] |\n"
    table_div = "+{0:-^14}+{0:-^18}+{0:-^21}+{0:-^22}+{0:-^18}+{0:-^18}+\n".format(*'-')

    f = open(file_path+'%s.txt' % (str(datetime.now())[:-7]), 'a+')
    f.write(text_input)

    # Table
    f.write(table_div)
    f.write(table_head)
    f.write(table_div)

    for i in range(len(acceptors)):
        table_line = "|{0: ^14}|{1: ^18}|{2: ^21}|{3: ^22.5f}|{4: ^18.3f}|{5: ^18.3f}|\n".format(acceptors[i], cant_decay[i],
                                                                                        cant_transf[i], efficiency[i],
                                                                                        walk_mean[i], total_time[i])
        f.write(table_line)

    f.write(table_div)
    f.close()


def extrac_from_list(a_list, column):
    return [x[column] for x in a_list]

def format_float_in_list(a_list):
    return ["%0.4f" % i for i in a_list]
