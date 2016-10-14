import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import integrate

# Datos experimentales a los cuales comprar
moleculas_quencher = 0, 9, 46, 82, 119, 156, 229, 351, 656, 1267, 2487,\
                     4929, 9289, 20190
cociente_tau = 1.000, 1.004, 1.489, 1.947, 2.429, 2.625, 3.320, 3.978, \
               5.363, 6.484, 7.371, 7.024, 7.820, 8.913
cociente_i = np.array([1.000, 1.061, 1.677, 2.117, 2.645, 3.031, 3.879,\
                       5.124, 6.840, 9.511, 11.775, 13.822, 16.141, 19.930])

eff_teo = 1 - cociente_i**(-1)

def bi_exp(x, a_1, b_1, a_2, b_2):
    return a_1**2  * np.exp(x / -b_1) + a_2**2 * np.exp(x / -b_2)
    
def bi_exp_norm(x, a_1, b_1, a_2, b_2, c):
    return (a_1**2 * np.exp(x / -b_1) + a_2**2 * np.exp(x / -b_2)) / c

def read_param_hist(path):
#Leemos los parametors del ajuste de ramiro, calculamos su area y se la
#agregamos como un parametro mas
    with open(path, 'r') as hist:
        line = hist.readline()
        param_hist_ramiro = []
        while line != '':
            line =' '.join(line.split())
            param = np.array(line.split(), dtype=np.float)
            area = integrate.quad(bi_exp, 0, np.inf,
                                  args=(param[1], param[2], param[3],
                                        param[4]))[0]
            param = param.tolist()
            param_hist_ramiro.append(np.array(param + [area]))
            line = hist.readline()
        return param_hist_ramiro
    
# Leemos los daots del hist.dat
'''
Lee el hist.dat, devuelve una lista con #aceptores y una lista de
arrays con los datos del histograma
'''        
def read_hist(path_hist):        
    with open(path_hist, 'r') as hist:
        line = hist.readline()
        num_aceptores = []
        decaimientos = []
        while line != '':
            values = list(eval(line))
            num_aceptores.append(values.pop(0))
            decaimientos.append(np.array(values))
            line = hist.readline()
        return(num_aceptores, decaimientos)

# Leemos el result.dat
def read_result(path_result):
    datos_quenching = open(path_result, 'r')
    line = datos_quenching.readline()
    while 'Traps number' not in line:
        line = datos_quenching.readline()
    junk, traps_number = line.split(': ')
    traps_number = eval(traps_number)
    while 'Acceptors number' not in line:
        line = datos_quenching.readline()
    junk, aceptors_number = line.split(': ')
    aceptors_number = eval(aceptors_number)
    while  not 'aceptores' in line and not 'Tiempo' in line:
        line = datos_quenching.readline()
        if 'Delta_t' in line:
            delta_t = (float(line.split(', ')[0].split(': ')[1]))
        if line == '':
            break
    lista_valores = []
    while True:
        line = datos_quenching.readline()
        if line == '\n':                    
            continue
        if '-'*10 in line:
            break
        # Removemos el enter al final de linea
        valores = '\t'.join(line.split('\n'))

        # Removemos todos los '\t'    
        valores = (' '.join(valores.split('\t')))
        # Removemos los espacios que nos quedan
        valores = np.array([float(valor) for valor in valores.split(' ') \
                            if valor != ''])
        lista_valores.append(valores)
        
    datos_quenching.close()
    return (lista_valores, delta_t)

def area_hist(decaimiento, delta_t):
    n, bins = np.histogram(decaimiento*delta_t, bins=max(decaimiento))
    popt, pcov = curve_fit(bi_exp, bins[:-1], n)
    area = popt[0]**2 * popt[1] + popt[2]**2 * popt[3]
    return area, popt

#param_ramiro = read_param_hist('param_hist_ramiro.dat')
#hist = read_hist('hist.dat')
#result = read_result('resul.dat')  

# Para los ultimos puntos se enoja con el error
# TypeError: Improper input: N=4 must not exceed M=2

#for param, decaimiento  in zip(param_ramiro, hist[1]):
#    x = np.linspace(0, 12, 50)
#    y_param = bi_exp_norm(x, param[1], param[2], param[3], param[4], param[-1])
#    area_dec, popt_dec = area_hist(decaimiento, result[1])
#    y_dec = bi_exp_norm(x, popt_dec[0], popt_dec[1], popt_dec[2], popt_dec[3], area_dec)
#    plt.plot(x, y_param, '-r', x, y_dec, 'g-')
#plt.show()
#    plt.semilogy(x, y)
    #print(integrate.quad(bi_exp_norm, 0, np.inf, args=(param[1], param[2], param[3], param[4], param[-1])))
#for decaimiento in hist[1]:
#    plt.hist(decaimiento, bins='auto')
    
#plt.show()
#    x = np.linspace(1, 90, 50)
#    area, popt = area_hist(decaimiento, result[1])
#    print(area, popt)
#    y = bi_exp_norm(x, popt[0], popt[1], popt[2], popt[3], area[0])
#    plt.plot(x, y, '--')
#plt.show()
#norm_hist(hist[1][0], result[1])