import pytest
import numpy as np

from ..aceptor import Aceptor


# Constructor tests
def test_constructor():
    aceptors = Aceptor(10, 1.3, 'sup')
    assert (aceptors.number == 10)


def test_constructor2():
    aceptors = Aceptor(10, 1.3, 'sup')
    assert (aceptors.way == 'sup')


def test_constructor3():
    aceptors = Aceptor(10, 1.3, 'vol')
    assert (aceptors.way == 'vol')


def test_constructor4():
    with pytest.raises(ValueError):
        aceptors = Aceptor(10, 1.3, 'volum')


# Representation test
def test_repr():
    traps = Aceptor(10, 1.3, 'vol')
    text_out = 'Number Aceptors: 10, R_Mechanisms: 1.3, way:vol'
    assert (text_out == str(traps))


# Generation tests
def test_generation_sup():
    NP_radio = 15
    aceptors = Aceptor(10, 1.3, 'sup')
    aceptors.generate(NP_radio)
    pos = aceptors.position
    r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
    np.testing.assert_allclose(r, NP_radio)


def test_generation_vol():
    NP_radio = 15
    aceptors = Aceptor(10, 1.3, 'vol')
    aceptors.generate(NP_radio)
    pos = aceptors.position
    r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
    all(r <= NP_radio) and all(r > 0)