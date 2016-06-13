import numpy as np

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


def __transfer_rate(exiton_pos, aceptors_pos, tau_d, r_forster):
    """
    Funcion para calcular la taza de transferencia a los aceptores
    intrinsicos o a los agregados.

    Parameters
    ----------
    exiton_pos : like array
        Posicion del exiton
    aceptors_pos : like array
        Posicion de todos los aceptores
    tau_d : float
        Tiempo de vida medio in ns
    r_forster : float
        Radio de Forster en nm
    """
    # constente usa para el calculo de k_et
    cte = r_forster**6/tau_d

    diff = exiton_pos - aceptors_pos
    component_square = diff*diff
    one_over_distance = 1/(component_square[:, 0] +
                           component_square[:, 1] +
                           component_square[:, 2])
    distance_6 = one_over_distance*one_over_distance*one_over_distance
    k = cte*sum(distance_6)
    return(k)


def forster(nanoparticle):
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
    check = 0
    amount_decay = 0
    amount_transf = 0
    num_walk = 0

    # Calculo de k
    k = 1/nanoparticle.tau_d

    while check == 0:

        # Calculo de k_et debido a los aceptores intrinsicos
        k_et_in = __transfer_rate(nanoparticle.exiton.position,
                                  nanoparticle.intrinsic_aceptors.position,
                                  nanoparticle.tau_d,
                                  nanoparticle.intrinsic_aceptors.r_forster)

        # Calculo de k_et debido a los aceptores agregados
        k_et_agre = __transfer_rate(nanoparticle.exiton.position,
                                    nanoparticle.aceptors.position,
                                    nanoparticle.tau_d,
                                    nanoparticle.aceptors.r_forster)

        # Taza total de tranferencia a cualqueir aceptor
        k_et = k_et_in + k_et_agre

        # Probabilidad de decaer por cualquier mecanismo
        prob_die = 1 - np.exp(-nanoparticle.delta_t * (k_et + k))

        # Eficiencia cuantica de transferencia
        psi_et = k_et/(k_et + k)

        if prob_die > np.random.random():
            if psi_et < np.random.random():
                amount_decay += 1
            else:
                amount_transf += 1
            check = 1
        else:
            nanoparticle.exiton.walk(nanoparticle.epsilon)
            num_walk += 1

    return(amount_transf, amount_decay, num_walk)


def boolean(nanoparticle):
    """
    El exiton se transfiere a un aceptor solo si esta
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
    """
    threshold = 0.5

    check = 0
    amount_decay = 0
    amount_transf = 0
    num_walk = 0

    # Taza de decaimiento natural
    k = 1/nanoparticle.tau_d
    # Probabilidad de decaer natural
    prob_natural = 1 - np.exp(-nanoparticle.delta_t * k)

    while check == 0:
        dif = nanoparticle.exiton.position - nanoparticle.aceptors.position
        dif2 = dif*dif
        distance = np.sqrt(dif2[:, 0] + dif2[:, 1] + dif2[:, 2])

        if np.any(distance < threshold):
            amount_transf += 1
            check = 1
        elif prob_natural > np.random.random():
            amount_decay += 1
            check = 1
        else:
            nanoparticle.exiton.walk(nanoparticle.epsilon)
            num_walk += 1

    return(amount_transf, amount_decay, num_walk)
