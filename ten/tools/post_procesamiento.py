import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate

# Datos experimentales a los cuales comprar
moleculas_quencher = 0, 9, 46, 82, 119, 156, 229, 351, 656, 1267, 2487,\
                     4929, 9289, 20190
cociente_tau = 1.000, 1.004, 1.489, 1.947, 2.429, 2.625, 3.320, 3.978, \
               5.363, 6.484, 7.371, 7.024, 7.820, 8.913
cociente_i = np.array([1.000, 1.061, 1.677, 2.117, 2.645, 3.031, 3.879,
                       5.124, 6.840, 9.511, 11.775, 13.822, 16.141, 19.930])

eff_teo = 1 - cociente_i**(-1)


def bi_exp(x, a_1, b_1, a_2, b_2):
    return a_1**2 * np.exp(x / -b_1) + a_2**2 * np.exp(x / -b_2)


def bi_exp_norm(x, a_1, b_1, a_2, b_2):
    c = a_1 * b_1 + a_2 * b_2

    return (a_1**2 * np.exp(x / -b_1) + a_2**2 * np.exp(x / -b_2)) / c


def read_param_hist(path):
    """
    Leemos los parametors del ajuste de ramiro, calculamos su area
    y se la agregamos como un parametro mas
    """
    with open(path, 'r') as hist:
        line = hist.readline()
        param_hist_ramiro = []
        while line != '':
            line = ' '.join(line.split())
            param = np.array(line.split(), dtype=np.float)
            area = integrate.quad(bi_exp, 0, np.inf,
                                  args=(param[1], param[2], param[3],
                                        param[4]))[0]
            param = param.tolist()
            param_hist_ramiro.append(np.array(param + [area]))
            line = hist.readline()
        return param_hist_ramiro


def read_hist(path_hist):
    """
    Lee el hist.dat, devuelve una lista con #aceptores y una lista de
    arrays con los datos del histograma
    """
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


def read_result(path_result):
    """

    Parameters
    ----------
    path_result: str
      Path to the result file

    Return
    ------
    results: like-list
      Results of the simulation
    parameters: like-list
      [delta_t, num traps, radio traps, mean free path]
    """
    datos = open(path_result, 'r')
    line = datos.readline()

    # Get the mean free path
    while 'Mean free path' not in line:
        line = datos.readline()
    junk, mean_path = line.split(': ')
    mean_path = eval(mean_path)

    # Get the number of traps
    while 'Traps number' not in line:
        line = datos.readline()
    junk, traps_number = line.split(': ')
    traps_number = eval(traps_number)

    # Get the radio of the traps
    while 'Traps mechanisms radius' not in line:
        line = datos.readline()
    junk, traps_radius = line.split(': ')
    traps_radius = eval(traps_radius)

    # Get the list of aceptors
    while 'Acceptors number' not in line:
        line = datos.readline()
    junk, aceptors_number = line.split(': ')
    aceptors_number = eval(aceptors_number)

    # Get delta_t
    while 'Delta_t' not in line:
        line = datos.readline()
    delta_t = (float(line.split(', ')[0].split(': ')[1]))

    # Go to the results
    while 'aceptores' not in line and 'Tiempo' not in line:
        line = datos.readline()
        if line == '':
            break

    results = []
    while True:
        line = datos.readline()
        if line == '\n':
            continue

        # End of the results
        if '-'*10 in line:
            break

        # Removemos el enter al final de linea
        valores = '\t'.join(line.split('\n'))
        # Removemos todos los '\t'
        valores = (' '.join(valores.split('\t')))
        # Removemos los espacios que nos quedan
        valores = np.array([float(valor) for valor in valores.split(' ')
                            if valor != ''])
        results.append(valores)

    datos.close()

    return (results, [delta_t, traps_number, traps_radius, mean_path])


def area_hist(decaimiento, delta_t):
    n, bins = np.histogram(decaimiento*delta_t, bins=max(decaimiento))
    popt, pcov = curve_fit(bi_exp, bins[:-1], n)
    area = popt[0]**2 * popt[1] + popt[2]**2 * popt[3]
    return area, popt
