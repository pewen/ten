"""
Random Number Functions
=======================

Este modulo implementa diferentes funciones relacionadas con numeros aleatorios


Utility functions
-----------------
random_walk          Paso de un caminante aleatorio
point_in_sphere      Genera n puntos en el volumen o la superficie
                     de una esfera

Poblations
----------
r_aceptors           Poblacion aleatoria de aceptores
r_nanoaprticles      Poblacion aleatoria de nanoparticulas
c_aceptors           Poblacion combinando los parametros
c_nanoparticles
x_aceptors
x_nanoparticles


TODO
----
* Poder setear una semilla
"""

from __future__ import absolute_import

from .base import points_in_sphere, set_seed
from .generator import random_walk
from .poblation import r_aceptors, r_nanoparticles, \
    c_aceptors, c_nanoparticles, \
    x_aceptors, x_nanoparticles

__all__ = ['points_in_sphere',
           'set_seed',
           'random_walk',
           'r_aceptors',
           'r_nanoparticles',
           'c_aceptors',
           'c_nanoparticles',
           'x_aceptors',
           'x_nanoparticles']
