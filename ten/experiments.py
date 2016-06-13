import time

import numpy as np

from .aceptor import Aceptor


"""
Distintos experimentos
"""


def quenching(nanoparticle, aceptors, mechanism, way,
              step=500, convergence=0.01):
    """
    Calcula la eficiencia de Quenching para una nanoparticula dada.


    Parameters
    ----------
    nanoparticle : NanoParticle Obj
        Nanoparticle to study.
    aceptors : Aceptor Obj
        Aceptors used to doped the nanoparticle.
    mechanism : function
        Forma de la transferencia.
    way : str
        Forma de general el exiton.
    step : float, optinal
        Numero de exitaciones que voy a hacer antes de
        chequear si converge o no.
    convergence : float, optional
        Diferencia con la simulacion anterior para definir
        si converge o no.


    Returns
    -------
    efficiency : float
        Quenching efficiency
    decay : float
        Mean of decay exitons
    walk_mean : float
        Mean number of walks
    exitations : float
        Total number of exitations
    total_time : float
        Total time


    Examples
    --------


    TODO
    ----
    - Controlar que el argumento way sea correcto.
    - Si el convergence es muy chico, podria no terminar nunca.
      Poner un valor para que corte el calculo.
    - Agregar ejempls.
    - Si el valor de la primera eficiencia calculada es menor
      que la diferencia, termina hay el experimento.
    """
    time_initial = time.time()

    exitations = 0
    efficiency_old = 0

    decay = 0
    transf = 0
    walk = 0

    while True:
        for cont in range(step):

            # Dopamiento
            nanoparticle.doped(aceptors)
            # Exitacion
            nanoparticle.excite(way)
            # Mecanismo de transferencia
            out = mechanism(nanoparticle)

            transf += out[0]
            decay += out[1]
            walk += out[2]

        exitations += step

        # Calculo la diferencia entre esta corrida y la anterior
        # Si es menor que convergence, termino el experimento.
        efficiency_new = transf/exitations
        diff = abs(efficiency_new - efficiency_old)
        if convergence > diff:
            break

        efficiency_old = efficiency_new

    walk_mean = walk/exitations
    total_time = time.time() - time_initial

    return(efficiency_new, decay, walk_mean, exitations, total_time)


def difusion_length(nanoparticle, mechanism, way='laser',
                    exitations=1500):
    """
    Calculated the exciton difusion length without any dopant.

    Se bombardea con varios exitones a la nanoparticula (sin dopar)
    y se guardan las posiciones donde se generan y las posiciones
    donde mueren. Luego, con estas posiciones se realiza un promedio RMS.


    Parametes
    ---------
    nanoparticle : NanoParticle Obj
        Nanoparticle to study.
    mechanism : function
        Forma de la transferencia
    exitations : float, optional
        Numero de exitaciones.


    Return
    ------
    l_d : float
        RMS value of the L_D
    exitations : float
        Total number of exitations
    total_time : float
        Total time


    Examples
    --------


    TODO
    ----
    - Controlar que el argumento way sea correcto
    - eliminar el numero de exitaciones y poner en funcion de convergence.
    - Si el convergence es muy chico, podria no terminar nunca, Poner un valor
    para que corte el calculo
    - Agregar ejemplos.
    """
    time_initial = time.time()

    positions_init = np.zeros((exitations, 3))
    positions_end = np.zeros((exitations, 3))
    dist = np.zeros(exitations)

    # Dopantes que le vamos a agregar a la NP
    dopantes = Aceptor(number=0, r_mechanisms=0, way='vol')
    # Dopamiento
    nanoparticle.doped(dopantes)

    for cont in range(exitations):
        # Excition
        nanoparticle.excite(way)

        positions_init[cont] = nanoparticle.exiton.position

        # Mecanismo de transferencia
        out = mechanism(nanoparticle)

        positions_end[cont] = nanoparticle.exiton.position

    diference2 = (positions_init - positions_end)*(positions_init -
                                                   positions_end)

    dist[:] = np.sqrt(diference2[:, 0] +
                      diference2[:, 1] +
                      diference2[:, 2])
    l_d = np.sqrt(sum(dist*dist)/exitations)

    total_time = time.time() - time_initial

    return(l_d, exitations, total_time)


def single_count(nanoparticle, aceptors, mechanism, way,
                 exitations=1500):
    """
    Count the number of walk of each exciton.
    This is use to estimate tau.

    Return
    ------
    walk_array : array
    Each element is the number of walk
    for each excitation.
    len(walk_array) = number of excitations

    Parameters
    ----------
    nanoparticle : NanoParticle Obj
        Nanoparticle to study.
    aceptors : Aceptor Obj
        Aceptors used to doped the nanoparticle.
    mechanism : function
        Forma de la transferencia.
    way : str
        Forma de general el exiton.
    exitations : float
        Total number of exitations


    Returns
    -------
    walks : array
        Cada elemento tiene la cantidad de pasos que realizo el
        exiton en cada exitacion. len(walks) == exitations.
    exitations : float
        Total number of exitations
    total_time : float
        Total time


    Examples
    --------


    Todo
    ----
    """
    time_initial = time.time()

    walks = np.zeros(exitations)

    # Dopo la NP
    nanoparticle.doped(aceptors)

    for i in range(exitations):
        # Excition
        nanoparticle.excite(way)
        # Mecanismo de transferencia
        out = mechanism(nanoparticle)

        walks[i] = out[2]

    total_time = time.time() - time_initial

    return(walks, exitations, total_time)


def tau():
    """

    """
    pass
