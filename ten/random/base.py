"""
Extended math utilities.
"""

from __future__ import division, absolute_import, print_function

from .generator import points_in_sphere_f90


def points_in_sphere(n_points, R, r=0):
    points = points_in_sphere_f90(n_points, R, r)

    return points
