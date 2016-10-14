"""
Extended math utilities.
"""

from __future__ import division, absolute_import, print_function

from numpy import random

from .generator import points_in_sphere_f90, init_random_seed


def points_in_sphere(n_points, R, r=0):
    points = points_in_sphere_f90(n_points, R, r)

    return points


def set_seed(seed):
    """
    Set seed for fortran and numpy random

    Parameters
    ----------
    """
    init_random_seed(seed)
    random.seed(seed)
