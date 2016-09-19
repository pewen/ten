"""
Functions that appears frequently in code
"""

from __future__ import division, absolute_import, print_function
from datetime import datetime
import platform
import sys


'''
def generate_random_points_in_sphere(n_points, R, r=0):
    """
    Return a array with the cordenades in cartesian for a
    point between two sphere of radio_out and radio_in.
    If R == r points are in the surface

    Parameters
    ----------
    n_points = int
        Number of points in sphere
    R : float
        Radio max of generate
    r : floar
        Radio min of generate. Default "0"

    Is not trivial generate random point in a sphere.
    See the ipython notebook in:
    ten/IPython_notebooks/Random_points_in_sphere.ipynb
    to understan why we generate for this form.
    """
    U = np.random.random(n_points)
    uniform_between_R_r = (R - r) * U**(1/3) + r

    X = np.random.randn(n_points, 3)
    randoms_versors = (np.sqrt(X[:, 0]**2 + X[:, 1]**2 +
                               X[:, 2]**2))**(-1) * X.T

    points_uniform_in_sphere = randoms_versors * uniform_between_R_r

    return points_uniform_in_sphere.T
'''


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
                    print("Sali del comentario multi linea")
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

        print(a)
        # Split the text and the value
        text, val = a.split(sep='=')

        # NP variables
        if text == 'r_mean':
            init_param['r_mean'] = float(val)
        elif text == 'r_desviation':
            init_param['r_desviation'] = float(val)
        elif text == 'tau_D':
            init_param['tau_D'] = float(val)
        elif text == 'mean_path':
            init_param['mean_path'] = float(val)
        elif text == 'epsilon':
            init_param['epsilon'] = float(val)

        # Instrinsic aceptors variables
        elif text == 'intrinsic_r_mechanisms':
            init_param['intrinsic_r_mechanisms'] = float(val)
        elif text == 'intrinsic_aceptors':
            init_param['intrinsic_aceptors'] = val
        elif text == 'intrinsic_way':
            init_param['intrinsic_way'] = val

        # Aceptors variables
        elif text == 'r_mechanisms':
            init_param['r_mechanisms'] = float(val)
        elif text == 'aceptors':
            init_param['aceptors'] = val
        elif text == 'way':
            init_param['way'] = val

        # Exiton variables
        elif text == 'exiton':
            init_param['exiton'] = val
        elif text == 'r_electro':
            init_param['r_electro'] = float(val)

        # Experiments variables
        elif text == 'experiments':
            init_param['experiments'] = val
        elif text == 'mechanisms':
            init_param['mechanisms'] = val
        elif text == 'excitations':
            init_param['excitations'] = float(val)
        else:
            print('Warning, the parameter {0} is not defined'.format(text))

    experiment_file.close()

    if init_param['exiton'] == 'elec' and 'r_electro' not in init_param:
        print('Error: If you generate the exiton by electrolysis,\
              you have to give a value of r_electro')
        sys.exit(-1)

    if 'r_deviation' not in init_param:
        init_param['r_deviation'] = 0

    return init_param


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
