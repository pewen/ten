"""
Funciones para generar poblaciones de aceptores y nanoparticulas
de formas aleatoria.


"""

from __future__ import division, absolute_import, print_function

import numpy as np


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


def r_nanoparticles(radio, tau, mean_path, epsilon, traps, sample):
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


def c_aceptors(numbers, r_mechanisms, ways):
    """
    Parameters
    ----------

    Return
    ------

    Todo
    ----
    """
    from ..core.aceptor import Aceptor

    out = []

    numbers_type = type(numbers)
    r_type = type(r_mechanisms)
    ways_type = type(ways)

    if numbers_type in [int, float]:
        numbers = [numbers]
    if r_type in [int, float]:
        r_mechanisms = [r_mechanisms]
    if ways_type in [str]:
        ways = [ways]

    for number in numbers:
        for radio in r_mechanisms:
            for way in ways:
                out.append(Aceptor(number, radio, way))

    return out


def c_nanoparticles(r_params, taus, mean_paths,
                    epsilons, traps, r_desviation=0):
    """
    Parameters
    ----------

    Return
    ------

    Todo
    ----
    """
    from ..core.nanoparticle import Nanoparticle

    if type(r_params) in [int, float]:
        r_params = [r_params]
    if type(taus) in [int, float]:
        taus = [taus]
    if type(mean_paths) in [int, float]:
        mean_paths = [mean_paths]
    if type(epsilons) in [int, float]:
        epsilons = [epsilons]

    out = []
    for radio in r_params:
        for tau in taus:
            for mean_path in mean_paths:
                for epsilon in epsilons:
                    for trap in traps:
                        out.append(Nanoparticle([radio, r_desviation], tau,
                                                mean_path, epsilon, trap))

    return out


def x_aceptors(numbers, r_mechanisms, ways, samples):
    """

    Parameters
    ----------
    number:

    r_mechanisms:

    ways:

    samples: like-array


    Return
    ------
    out: list
      List with the aceptors

    Example
    -------
    >>> numbers = [2, 12]
    >>> r_mechanisms = [0.3, 0.7]
    >>> ways = ['vol', 'sup']
    >>> samples = [5, 5, 2]
    >>> traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    >>> len(traps)
    50

    # Si samples es un int, se utiliza el mismo valor para
    # numbers y r_mechanisms
    >>> numbers = [2, 12]
    >>> r_mechanisms = [0.3, 0.7]
    >>> ways = ['vol', 'sup']
    >>> samples = 5 # igual a samples = [5, 5, 2]
    >>> traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    >>> len(traps)
    50
    """
    if type(samples) in [int, float]:
        samples = [int(samples), int(samples)]
    if len(samples) == 1:
        samples = [int(samples[0]), int(samples[0])]

    if type(numbers) in [int, float]:
        numbers = [numbers]
        samples[0] = 1
    if type(r_mechanisms) in [int, float]:
        r_mechanisms = [r_mechanisms]
        samples[1] = 1
    if type(ways) in [str]:
        ways = [ways]

    numbers = __equi_sample(numbers, samples[0])
    numbers = [round(num) for num in numbers]
    r_mechanisms = __equi_sample(r_mechanisms, samples[1])

    out = c_aceptors(numbers, r_mechanisms, ways)

    return out


def x_nanoparticles(radios, taus, mean_paths, epsilons, traps, samples):
    """


    Parameters
    ----------


    Return
    ------


    Example
    -------
    >>> r_np = 15
    >>> taus = 0.333
    >>> mean_paths = [70, 120]
    >>> epsilons = 1
    >>> traps = traps
    >>> samples = 2
    >>> nanos = ten.random.x_nanoparticles(r_np, taus, mean_paths, epsilons, traps, samples)
    >>> len(nanos)
    50
    """
    if type(samples) in [int, float]:
        samples = [int(samples) for x in range(4)]
    if len(samples) == 1:
        samples = [int(samples[0]) for x in range(4)]

    if type(radios) in [int, float]:
        radios = [radios]
        samples[0] = 1
    if type(taus) in [int, float]:
        taus = [taus]
        samples[1] = 1
    if type(mean_paths) in [int, float]:
        mean_paths = [mean_paths]
        samples[2] = 1
    if type(epsilons) in [int, float]:
        epsilons = [epsilons]
        samples[3] = 1

    radios = __equi_sample(radios, samples[0])
    taus = __equi_sample(taus, samples[1])
    mean_paths = __equi_sample(mean_paths, samples[2])
    epsilons = __equi_sample(epsilons, samples[3])

    out = c_nanoparticles(radios, taus, mean_paths,
                          epsilons, traps)
    return out


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


def __equi_sample(extrems, sample):
    """
    Dado los limites para una variable, genero n muestras equiproables

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
    # Me fijo si es una lista con un solo elemento
    if len(extrems) == 1:
        out = [extrems[0] for x in range(sample)]
    # Sino, genero los r_mecha con una distribucion uniforme
    else:
        out = np.linspace(extrems[0], extrems[1], sample)

    return out
