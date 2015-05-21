"""
Functions that appears frequently in code
"""
import numpy as np

def generate_random_points_in_sphere(n_points, R, r=0):
    """
    Return a array with the cordenades in cartesian for a point between two sphere of radio_out and radio_in.
    If R == r points are in the surface

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

    X = np.random.randn(n_points, 3)
    randoms_versors = ( np.sqrt(X[:,0]**2 + X[:,1]**2 + X[:,2]**2) )**( -1 ) * X.T

    points_uniform_in_sphere = randoms_versors * uniform_between_R_r

    return points_uniform_in_sphere.T

def read4file(file_path):
    """
    Read the initial parameter for a file.
    The file can have multiple lines of comments, always, starting with "" "and end with" "". In addition, the symbol # is considered line comment. This symbol can be used, for example, after declaring the value of a variable to a comment it.

    Parameters
    ----------
    file_path : str
        Path to the file
    """
    f = open(file_path, 'r')

    init_param = {}
    
    while True:
        a = f.readline()
    
        #salteo todo los comentarios que usan """
        if '"""' in a:
            while True:
                #print(a)
                a = f.readline()
                if '"""' in a:
                    a = f.readline()
                    break
                
        #salteo todo los comentarios que usan '''
        elif "'''" in a:
            while True:
                #print(a)
                a = f.readline()
                if "'''" in a:
                    a = f.readline()
                    break
    
        if a == '\n':
            a = f.readline()
        
        if a == '':
            break
        
        #Remove all spaces
        a = ''.join(a.split())

        #Remove all comment with "#" 
        if '#' in a:
            a, rest = a.split('#')
    
        #Split the text and the value
        text, val = a.split(sep='=')
        #variables
        if text == 'r':
            init_param['r'] = float(val)
        elif text == 'R_Forster':
            init_param['R_Forster'] = float(val)
        elif text == 'L_D':
            init_param['L_D'] = float(val)
        elif text == 'tau_D':
            init_param['tau_D'] = float(val)
        elif text == 'num_acceptors':
            init_param['num_acceptors'] = int(val)
        elif text == 'delta_t':
            init_param['delta_t'] = float(val)
        elif text == 'num_exc':
            init_param['num_exc'] = int(val)
        elif text == 'acceptors':
            init_param['acceptors'] = val
        elif text == 'exiton':
            init_param['exiton'] = val
        elif text == 'r_electro':
            init_param['r_electro'] = float(val)
        else:
            print('No es nada de esto')
        
    f.close()

    return init_param
