import matplotlib.pyplot as plt

import sys

sys.path.append('../')

from src.nanoparticle import NanoParticle
from src.exciton import Exciton

def lab(r, R_Forster, L_DS, tau_D, epsilon, num_exc, aceptores):
    result = []
    for L_D in L_DS:
        print('L_D de ', L_D, 'nm. Numero de aceptores: ', end='')
        delta_t = (epsilon * tau_D) / L_D
        
        input_parameters = []
        output_parameters = []

        #for num_acceptors in linspace(num_acceptors_min, num_acceptors_max, num_simu):
        for num_acceptors in aceptores:
            print(num_acceptors, ', ', end='')
            num_acceptors = int(num_acceptors)
            nano_particle = NanoParticle(r, num_acceptors, tau_D, R_Forster, L_D, delta_t, 'vol')

            simu = Exciton(nano_particle, num_exc, 'laser')
            simu.calculate()
            input_parameters += [simu.get_input()]
            output_parameters += [simu.get_output()]

        eff_simu = [[element[4] for element in output_parameters], L_D]
        result += eff_simu
        print()   
    return result

def plot_lab(result, aceptores, eff, title):
    l_ds = [result[i+1] for i in range(0, len(result), 2)]
    for i in range(0, len(result), 2):
        plt.plot(aceptores, result[i], 'o--')
    plt.plot(aceptores, eff, 'o-')
    plt.grid()
    plt.xlim(-10, 1010)
    plt.ylim(-0.1, 1.1)
    plt.title(title)
    plt.xlabel('Number of acceptors')
    plt.ylabel('Quenching Efficiency')
    l_ds = ['L_D = ' + str(i) for i in l_ds]
    plt.legend(l_ds + ['L_D real'], loc=0)
    plt.show()

'''
import numpy as np

exp = np.array(eff2)
minimo = [100, 0]
for i in range(0, len(result), 2):
    valor = np.array(result[i])
    if minimo[0] > sum((exp - valor)**2):
        minimo[0] = sum((exp - valor)**2)
        minimo[1] = result[i+1]
print(minimo)
'''