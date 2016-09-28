import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Datos experimentales a los cuales comprar
moleculas_quencher = 0, 9, 46, 82, 119, 156, 229, 351, 656, 1267, 2487,\
                     4929, 9289, 20190
cociente_tau = 1.000, 1.004, 1.489, 1.947, 2.429, 2.625, 3.320, 3.978, \
               5.363, 6.484, 7.371, 7.024, 7.820, 8.913
cociente_i = 1.000, 1.061, 1.677, 2.117, 2.645, 3.031, 3.879, 5.124, \
             6.840, 9.511, 11.775, 13.822, 16.141, 19.930

# Leemos los parametors del ajuste de ramiro
with open('param_hist_ramiro.dat', 'r') as hist:
    line = hist.readline()
    param_hist_ramiro = []
    while line != '':
        line =' '.join(line.split())
        param = np.array(line.split(), dtype=np.float)
        param_hist_ramiro.append(param)
        line = hist.readline()
    
# Leemos los daots del hist.dat
with open('hist.dat', 'r') as hist:
    line = hist.readline()
    num_aceptores = []
    decaimientos = []
    while line != '':
        values = list(eval(line))
        num_aceptores.append(values.pop(0))
        decaimientos.append(np.array(values))
        line = hist.readline()

# Leemos el result.dat
datos_quenching = open('result.dat', 'r')
line = datos_quenching.readline()
while 'Traps number' not in line:
    line = datos_quenching.readline()
junk, traps_number = line.split(': ')
traps_number = eval(traps_number)
while 'Acceptors number' not in line:
    line = datos_quenching.readline()
junk, aceptors_number = line.split(': ')
aceptors_number = eval(aceptors_number)
datos_lindos = []
deltas_t = []
while line != '':
    while  not 'Aceptores' in line and not 'Tiempo' in line:
        if 'Delta_t' in line:
            deltas_t.append(float(line.split(', ')[0].split(': ')[1]))
        cant_filas = 0
        datos = []
        line = datos_quenching.readline()
    while '-'*10 not in line:
        line = datos_quenching.readline()
        cant_filas += 1
        datos += line
    valor = ''
    dato_lindo = []
    for dato in datos:
        if dato == '\t' :
            dato_lindo.append(valor)
            valor = ''
            continue
        if dato == ' ' or dato == '\n':
            continue
        valor += dato
    datos_lindos.append(dato_lindo)
    line = datos_quenching.readline()
    if line == '':
        break

datos_array = [datos.reshape(len(aceptors_number), 8) for datos in \
               np.array(datos_lindos, dtype=np.float)]        
datos_quenching.close()

plt.subplot(2, 2, 1)
for i in range(len(traps_number)):
        plt.plot(aceptors_number, datos_array[i][:, 4], 'o--')
plt.legend(traps_number, loc=0, title='Cantidad trampas')
plt.xlabel('Cantidad aceptores')
plt.ylabel('Eficiencia')
plt.grid()

# Graficamos el decaimiento
def func(x, a_1, b_1, a_2, b_2, c):
    return a_1 * np.exp(-b_1 * x) + a_2 * np.exp(-b_2 * x) + c

plt.subplot(2, 2, 2)
for i, parametros in enumerate([[x, y] for x in zip(traps_number, deltas_t) \
                                for y in aceptors_number]):
    n, bins = np.histogram(decaimientos[i]*parametros[0][1], bins='auto', normed=1)
    popt, pcov = curve_fit(func, bins[:-1], n)
    plt.plot(func(bins, *popt), linewidth=4,
             label="{0}, {1}".format(parametros[0][0], parametros[1]))
plt.grid()
plt.legend(loc=0, ncol=3, title='# trampas, # aceptores')
plt.subplot(2, 2, 3)
for i, param in enumerate(param_hist_ramiro):
    x = np.linspace(1, 90, 50)
    y = func(x, param[1], param[2], param[3], param[4], param[0])
    plt.plot(x, y, label="Ajuste sub{0}".format(i))
plt.show()