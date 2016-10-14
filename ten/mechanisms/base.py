import numpy as np

from .forster_mecha import forster_mecha


"""
Se definen distintos mecanismos por los que puede decaer un exiton
(algo similar a los potenciales en LAMPS). La idea es que el usuario
puede usar alguno de los mecanismos implementados aca, o puede
escribir su propio mecanismo.

Para todos los mecanismo de trasnferencia, los requisitos son:

Parameters
----------
nanoparticle : NanoParticle Obj
    NanoParticle to study

Returns
-------
amount_transf : float
    Number of total transfed exitons
amount_decay : float
    Number of total decay exitons
num_walks : float
    Number of total walks
"""


def forster(NP):
    """
    Mecanismo de transferencia del tipo Forster.

    The energy transfer rate constant (k_et) is defined as:
    k_et = sum ((1 / tau_d)*(R_0 / r[i]) ** 6)
    where r[i] is the distance between the exciton
    and each acceptor and R_0 is the Forster radius.
    The sum go from 1 to M where M is the number of acceptors.

    The radiative transfer rate (k_r) and nonradioactive
    transfer rate (k_nr) is defined as
    k = k_r + k_nr = 1/tau_d

    Then, the probability of the exiton die is
    prob_die = 1 - e**(-delta_t * [k_et + k])

    The quantum efficiency of transfer is defined as:
    psi_et = k_et/(k_et + k)

    Parameters
    ----------
    nanoparticle: NanoParticle Obj

    Returns
    -------
    amount_transf : float
        Number of total trasnference exiton
    amount_decay : float
        Number of total decay exiton
    num_walks : float
        Number of total walks

    TODO
    ----
    - Hacer ejemplos.
    """
    out = forster_mecha(NP.exiton.position, NP.aceptors.position,
                        NP.aceptors.r_mechanisms, NP.traps.position,
                        NP.traps.r_mechanisms, NP.tau_d, NP.delta_t,
                        NP.radio, NP.epsilon)

    return out


def dexter(nanoparticle):
    """
    El exiton se transfiere a algun aceptor si y solo si esta
    menos de cierta distancia (threshold).

    Parameters
    ----------
    nanoparticle: NanoParticle Obj

    Returns
    -------
    amount_transf : float
        Number of total trasnference exiton
    amount_decay : float
        Number of total decay exiton
    num_walks : float
        Number of total walks

    TODO
    ----
    - Hacer ejemplos.
    - Pasar la funcion a fortran
    """
    check = 0
    amount_decay = 0
    amount_transf = 0
    num_walk = 0

    # Taza de decaimiento natural
    k = 1/nanoparticle.tau_d
    # Probabilidad de decaer natural
    prob_natural = 1 - np.exp(-nanoparticle.delta_t * k)

    while check == 0:
        bool_intri = __distance(nanoparticle.exiton.position,
                                nanoparticle.traps.position,
                                nanoparticle.traps.r_mechanisms)

        bool_aceptors = __distance(nanoparticle.exiton.position,
                                   nanoparticle.aceptors.position,
                                   nanoparticle.aceptors.r_mechanisms)

        if bool_intri or bool_aceptors:
            amount_transf += 1
            check = 1
        elif prob_natural > np.random.random():
            amount_decay += 1
            check = 1
        else:
            nanoparticle.exiton.walk(nanoparticle.epsilon)
            num_walk += 1

    return(amount_transf, amount_decay, num_walk)


def __distance(exiton_pos, aceptors_pos, threshold):
    """
    Retorna True si la distancia euclidea entre el exiton
    y algun aceptor es menor que threshold.
    False en el caso contrario.

    Parameters
    ----------
    exiton_pos : array
        Posicion del exiton
    aceptors_pos : array
        Posicion de todos los aceptores
    threshold : float
        Distancia a comparar

    Returns
    -------
    out : bool
        True si la distancia del exiton a algun aceptor es menor que threshold.
        False caso contrario.
    """
    dif = exiton_pos - aceptors_pos
    dif2 = dif*dif
    distance = np.sqrt(dif2[:, 0] + dif2[:, 1] + dif2[:, 2])

    out = np.any(distance < threshold)

    return out