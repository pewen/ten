"""
Funciones para generar poblaciones de aceptores y nanoparticulas
de formas aleatoria.
"""

from __future__ import division, absolute_import, print_function

import numpy as np


def __uniform_sample(extrems, sample):
    """
    Dada una lista de dos elementos, genero n valores aleatorios
    entre esos valores

    Parameters
    ----------
    extrems: like-list
      [lim inf, lim sup] entre los que generar los valores aleatorios
    sample: int
      Numero de muestras

    Return
    ------
    out: list
      Lista con los valores aleatorios
    """
    data_type = type(extrems)

    # Me fijo si el r_mecha es constante
    if data_type in [int, float]:
        out = [extrems for x in range(sample)]
    # Me fijo si es una lista con un solo elemento
    elif len(extrems) == 1:
        out = [extrems[0] for x in range(sample)]
    # Sino, genero los r_mecha con una distribucion uniforme
    else:
        out = [(extrems[1] - extrems[0]) * np.random.random_sample()
               + extrems[0] for x in range(sample)]

    return out


def r_aceptors(number, r_mechanisms, way, sample):        
    """
    Genera una poblacion aleatoria de aceptores.

    Si algun valor es contante, se lo puede pasar sin la lista.

    Parameters
    ----------
    number: like-list
      [lim inf, lim sup] del numero de aceptores
    r_mechanisms: like-list
      [lim inf, lim sup] del radio del mecanismo
    way: like-list
      ['way1', 'way2'] distintas posibles formas de dopar
    sample: int
      Numero de elemntos a generar

    Return
    ------
    out: list
      Lista con los aceptores aleatorios

    Exampels
    --------

    TODO
    ----
    * ejemplos
    """
    from ..core.aceptor import Aceptor

    number_type = type(number)
    way_type = type(way)

    # Random de los r_mecha
    radius = __uniform_sample(r_mechanisms, sample)

    # Random de la cantidad de trampas
    if number_type in [int, float]:
        numbers = np.array([number for x in range(sample)])
    elif len(number) == 1:
        numbers = np.array([number[0] for x in range(sample)])
    else:
        numbers = np.random.randint(number[0], number[1]+1, sample)

    # Random de la forma de generacion
    if way_type == str:
        ways = [way for x in range(sample)]
    elif len(way) == 1:
        ways = [way[0] for x in range(sample)]
    else:
        val = []
        for i in range(sample):
            val.append(np.random.randint(len(way)))

        ways = [way[i] for i in val]

    out = []
    for number, radio, way in zip(numbers, radius, ways):
        out.append(Aceptor(number, radio, way))

    return out


def r_nanoparticle(radio, tau, mean_path, epsilon, traps, sample):
    """
    Genera una poblacion aleatoria de nanoparticulas

    Parameters
    ----------
    radio: like-list
      [lim inf, lim sup] en los que generar el radio de la np
    tau: like-list
      [lim inf, lim sup] en los que generar los taus
    mean_path: like-list
      [lim inf, lim sup] en los que generar los mean_free_path
    epsilon: like-list
      [lim inf, lim sup] en los que generar los epsilon
    traps: list
      Lista con las trampas de cada aceptor
    sample: int
      Numero de muestras.

    Return
    ------
    out: list
      Lista con las nanoparticulas aleatorias

    Examples
    --------

    Todo
    ----
    * ejemplos
    * que se peuda pasar una sola conf de aceptores y que dope a todos
      con ese solo.
    """
    from ..core.nanoparticle import Nanoparticle
    
    radius = __uniform_sample(radio, sample)
    taus = __uniform_sample(tau, sample)
    means = __uniform_sample(mean_path, sample)
    epsilons = __uniform_sample(epsilon, sample)

    out = []
    for r, tau, mean, e, trap in zip(radius, taus, means, epsilons, traps):
        out.append(Nanoparticle(r, tau, mean, e, trap))

    return out
