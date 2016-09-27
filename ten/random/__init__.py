"""
Random Number Functions
=======================

Este modulo implementa diferentes funciones relacionadas con numeros aleatorios


Utility functions
-----------------
random_walk          Paso de un caminante aleatorio
point_in_sphere      Genera n puntos en el volumen o la superficie
                     de una esfera

TODO
----
* Poder setear una semilla
"""

from .base import points_in_sphere
from .generator import random_walk

__all__ = ['points_in_sphere', 'random_walk']
