import pytest
import numpy as np

from ..exciter import Exciter
from ...random import set_seed


def test_constructor():
    exiton = Exciter('laser', 15)
    assert(exiton.way == 'laser')


def test_constructor2():
    exiton = Exciter('laser', 15)
    assert(exiton.r_electro == 0)


def test_constructor3():
    exiton = Exciter('laser', 15)
    assert(exiton.np_radio == 15)


def test_constructor4():
    with pytest.raises(ValueError):
        Exciter('elec', 15)


def test_constructor5():
    with pytest.warns(RuntimeWarning):
        Exciter('electro', 15)


def test_laser():
    set_seed(8)
    exiton = Exciter('laser', 15)
    exiton.laser_generated()
    pos = np.array([3.48097515, -0.26103414, 6.16735347])
    np.testing.assert_allclose(exiton.position, pos)


def test_generated():
    set_seed(8)
    exiton = Exciter('laser', 15, 13)
    exiton.electro_generated()
    pos = [6.84969176,  -0.51365015,  12.13581494]
    np.testing.assert_allclose(exiton.position, pos)


def test_walk():
    np_radio = 15
    exiton = Exciter('laser', np_radio)
    for i in range(4000):
        exiton.walk(2)
    np.sqrt(sum(exiton.position**2)) < np_radio
