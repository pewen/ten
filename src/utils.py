"""
Functions that appears frequently in code
"""
import numpy as np

def generate_random_points_in_sphere(n_points, R, r=0):
    """
    Return a array with the cordenades in cartesian for a point between two sphere of radio_out and radio_in.

    Parameters
    ----------
    n_points = int
        Number of points in sphere
    R : float
        Radio max of generate
    r : floar
        Radio min of generate. Default "0"

    Is not trivial generate random point in a sphere.
    See the ipython notebook in: ten/doc/notebooks/Random_points_in_sphere.ipynb to understan why we generate for this form.
    """
    
    U = np.random.random(n_points)
    uniform_between_R_r = (R - r) * U**(1/3) + r
    
    X = np.random.randn(3, n_points)
    randoms_versors = ( np.sqrt(X[0]**2 + X[1]**2 + X[2]**2) )**( -1 ) * X

    points_uniform_in_sphere = uniform_between_R_r * randoms_versors

    return points_uniform_in_sphere
    
