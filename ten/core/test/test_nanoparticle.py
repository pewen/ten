import numpy as np

from ..nanoparticle import Nanoparticle
from ..aceptor import Aceptor


# Constructor tests
def test_constructor():
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=[11.25, 0], tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert(NP.r_param == [11.25, 0])


def test_constructor2():
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=11.25, tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert(NP.radio == 11.25)


def test_constructor3():
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=[11.25], tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert(NP.r_param == [11.25, 0])


def test_constructor4():
    np.random.seed(2)
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=[11.25, 0.3], tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert(NP.radio == 11.124972645778358)


def test_constructor5():
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=[11.25, 0], tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert([NP.tau_d, NP.mean_path, NP.epsilon] == [0.333, 100, 1])


def test_constructor6():
    # Trampas (dopantes intrisicos) de la NP
    trampas = Aceptor(number=1, r_mechanisms=1, way='vol')
    # Nanoparticula
    NP = Nanoparticle(r_param=[11.25, 0], tau_d=0.333,
                      mean_path=100, epsilon=1, traps=trampas)
    assert([NP.delta_t, NP.p_decay] == [0.00333, 0.009950166250831893])


# Representation tests
def test_repr():
    traps = Aceptor(10, 1.3, 'vol')
    NP = Nanoparticle([15, 0], 0.333, 50, 1, traps)
    out_text = """Radio: 15 ~ U(15, 0),
Tau: 0.333, Mean_path: 50, Epsilon: 1,
Delta_t: 0.00666, Prob decay: 0.01980132669,
Number traps: 10, R_Mechanisms: 1.3, way: vol"""

    assert (out_text == str(NP))


def test_repr2():
    np.random.seed(2)
    traps = Aceptor(10, 1.3, 'vol')
    NP = Nanoparticle([15, 0.5], 0.333, 50, 1, traps)
    out_text = """Radio: 14.791621076297265 ~ U(15, 0.5),
Tau: 0.333, Mean_path: 50, Epsilon: 1,
Delta_t: 0.00666, Prob decay: 0.01980132669,
Number traps: 10, R_Mechanisms: 1.3, way: vol"""

    assert(out_text == str(NP))


def test_repr3():
    np.random.seed(2)
    traps = Aceptor(10, 1.3, 'vol')
    dopantes = Aceptor(50, 3, 'vol')
    NP = Nanoparticle([15, 0.5], 0.333, 50, 1, traps)
    NP.doped(dopantes)
    out_text = """Radio: 14.791621076297265 ~ U(15, 0.5),
Tau: 0.333, Mean_path: 50, Epsilon: 1,
Delta_t: 0.00666, Prob decay: 0.01980132669,
Number traps: 10, R_Mechanisms: 1.3, way: vol
Number Aceptors: 50, R_Mechanisms: 3, way:vol"""

    assert(out_text == str(NP))


def test_repr4():
    np.random.seed(2)
    traps = Aceptor(10, 1.3, 'vol')
    dopantes = Aceptor(50, 3, 'vol')
    NP = Nanoparticle([15, 0.5], 0.333, 50, 1, traps)
    NP.doped(dopantes)
    NP.excite('laser')
    out_text = """Radio: 14.791621076297265 ~ U(15, 0.5),
Tau: 0.333, Mean_path: 50, Epsilon: 1,
Delta_t: 0.00666, Prob decay: 0.01980132669,
Number traps: 10, R_Mechanisms: 1.3, way: vol
Number Aceptors: 50, R_Mechanisms: 3, way:vol
Exition way: laser, R_electro: 0"""

    assert(out_text == str(NP))


# Deped tests
def test_doped_sup():
    np.random.seed(2)
    traps = Aceptor(10, 1.3, 'vol')
    dopantes = Aceptor(10, 3.2, 'sup')
    NP = Nanoparticle([15, 0], 0.333, 50, 1, traps)
    NP.doped(dopantes)
    pos = NP.aceptors.position
    r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
    np.testing.assert_allclose(r, 15)


def test_doped_vol():
    traps = Aceptor(10, 1.3, 'vol')
    dopantes = Aceptor(4, 3.2, 'vol')
    NP = Nanoparticle([15, 0.5], 0.333, 50, 1, traps)
    np.random.seed(2)
    NP.doped(dopantes)
    out = np.array([[-9.97994851,  -4.68407978,   2.79838913],
                    [-2.95667238,  -2.5118831,  -2.15824574],
                    [2.87360327,  11.94459721,   0.21645999],
                    [-9.23033613,   4.45082408,  -4.92229105]])
    (NP.aceptors.position == out).all()
