"""
Functions that appears frequently in code
"""
import numpy as np

def generate_random_points_in_sphere(n_points, radio):
    """
    Return a array with the cordenades in cartesian for a point in a sphere of radio 'radio'
    Is not trivial generate random point in a sphere.
    See the ipython notebook in: ten/doc/notebooks/Random_points_in_sphere.ipynb to understan why we generate for this form.
    """
    U = np.random.random(n_points)
    X = np.random.randn(3, n_points)

    points_uniform_in_sphere = (radio * U**(1/3) / np.sqrt(X[0]**2 + X[1]**2 + X[2]**2) ) * X

    return points_uniform_in_sphere
    
