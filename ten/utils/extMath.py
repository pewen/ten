"""
Extended math utilities.
"""

from __future__ import division, absolute_import, print_function

import numpy as np

from .random import points_in_sphere


def random_points_in_sphere(n_points, R, r=0):
    if n_points == 0:
        points = np.random.randn(0, 3)
        return points

    points = points_in_sphere(n_points, R, r)

    return points
