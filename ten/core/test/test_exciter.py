import pytest
import numpy as np

from ..exciter import Exciter


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
