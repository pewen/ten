#! /usr/bin/env python3

from numpy import e
from numpy.random import normal

from .exciter import Exciter


class Nanoparticle(object):
    """
    Nanoaprticle object
    """

    def __init__(self, r_param, tau_d, mean_path, epsilon, intrinsic_aceptors):
        """
        Create a NanoParticle object.

        Parameters
        ----------
        r_param : list_like
            [mean_normal, mean_desviation] NP radio normal distribution in nm.
            If not mean_desviation, the radio is considered constant.
        tau_d : float
            Lifetime of the donor. [tau_D] = ns.
        mean_path : float
            Length of mean free path. [mean_path] = nm.
        epsilon : float
            Step length on the random walk. [epsilon] = nm.
        intrinsic_aceptors : Aceptor
            Aceptores propios de la NP.

        Returns
        -------
        out : nanoparticle
            An NanoParticle object.

        Examples
        --------
        """
        # NanoParticle paremeters
        self.r_param = r_param

        if r_param[1] == 0:
            self.radio = r_param[0]
        else:
            self.radio = normal(r_param[0], r_param[1])

        self.tau_d = tau_d
        self.mean_path = mean_path
        self.epsilon = epsilon

        self.delta_t = (epsilon*tau_d)/mean_path

        # Decay probability
        self.p_decay = 1 - e**(-self.delta_t/tau_d)

        # Aceptores intrisicos
        self.intrinsic_aceptors = intrinsic_aceptors
        self.intrinsic_aceptors.generate(self.radio)

        self.aceptors = 'NP is not doped'
        self.exiton = 'NP is not exited'

    def __str__(self):
        """
        Prity print of the NanoParticle

        Examples
        --------
        >>> from aceptor import Aceptor
        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> NP = Nanoparticle([15, 0], 0.333, 50, 1, dopantes_propios)
        >>> print(NP)
        Radio: 15 ~ U(15, 0),
        Tau: 0.333, Mean_path: 50, Epsilon: 1,
        Delta_t: 0.00666, Prob decay: 0.019801326693244747,
        Nº Intrisic aceptors: 10, R_Forster: 1.3, way: vol

        >>> import numpy as np
        >>> from aceptor import Aceptor
        >>> np.random.seed(2)
        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> NP = Nanoparticle([15, 0.5], 0.333, 50, 1, dopantes_propios)
        >>> print(NP)
        Radio: 14.791621076297265 ~ U(15, 0.5),
        Tau: 0.333, Mean_path: 50, Epsilon: 1,
        Delta_t: 0.00666, Prob decay: 0.019801326693244747,
        Nº Intrisic aceptors: 10, R_Forster: 1.3, way: vol

        >>> import numpy as np
        >>> from aceptor import Aceptor
        >>> np.random.seed(2)
        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> dopantes = Aceptor(50, 3, 'vol')
        >>> NP = Nanoparticle([15, 0.5], 0.333, 50, 1, dopantes_propios)
        >>> NP.doped(dopantes)
        >>> print(NP)
        Radio: 14.791621076297265 ~ U(15, 0.5),
        Tau: 0.333, Mean_path: 50, Epsilon: 1,
        Delta_t: 0.00666, Prob decay: 0.019801326693244747,
        Nº Intrisic aceptors: 10, R_Forster: 1.3, way: vol
        Nº Aceptors: 50, R_Forster: 3, way:vol

        >>> import numpy as np
        >>> from aceptor import Aceptor
        >>> np.random.seed(2)
        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> dopantes = Aceptor(50, 3, 'vol')
        >>> NP = Nanoparticle([15, 0.5], 0.333, 50, 1, dopantes_propios)
        >>> NP.doped(dopantes)
        >>> NP.excite('laser')
        >>> print(NP)
        Radio: 14.791621076297265 ~ U(15, 0.5),
        Tau: 0.333, Mean_path: 50, Epsilon: 1,
        Delta_t: 0.00666, Prob decay: 0.019801326693244747,
        Nº Intrisic aceptors: 10, R_Forster: 1.3, way: vol
        Nº Aceptors: 50, R_Forster: 3, way:vol
        Exition way: laser, R_electro: 0

        """

        number = self.intrinsic_aceptors.number
        forster = self.intrinsic_aceptors.r_forster
        way = self.intrinsic_aceptors.way

        # NP general information
        representation = """Radio: {0} ~ U({6}, {7}),
Tau: {1}, Mean_path: {2}, Epsilon: {3},
Delta_t: {4}, Prob decay: {5},
Nº Intrisic aceptors: {8}, R_Forster: {9}, way: {10}""".format(self.radio,
                                                               self.tau_d,
                                                               self.mean_path,
                                                               self.epsilon,
                                                               self.delta_t,
                                                               self.p_decay,
                                                               self.r_param[0],
                                                               self.r_param[1],
                                                               number,
                                                               forster,
                                                               way)

        # NP doped information
        if self.aceptors != 'NP is not doped':
            rep_aceptors = """
Nº Aceptors: {0}, R_Forster: {1}, way:{2}""".format(self.aceptors.number,
                                                    self.aceptors.r_forster,
                                                    self.aceptors.way)
            representation = representation + rep_aceptors

        # NP exited information
        if self.exiton != 'NP is not exited':
            rep_exiton = """
Exition way: {0}, R_electro: {1}""".format(self.exiton.way,
                                           self.exiton.r_electro)
            representation = representation + rep_exiton

        return(representation)

    def doped(self, aceptors):
        """
        Depositing surface or volumetrically acceptors on the nanoparticle.

        Parameters
        ----------
        aceptors : Aceptor
            Aceptores que se van a usar para podar

        Examples
        --------
        Necesary imports

        >>> import numpy as np
        >>> from nanoparticle import Nanoparticle
        >>> from aceptor import Aceptor

        Sup doped

        >>> np.random.seed(2)
        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> dopantes = Aceptor(10, 3.2, 'sup')
        >>> NP = Nanoparticle([15, 0], 0.333, 50, 1, dopantes_propios)
        >>> NP.doped(dopantes)
        >>> pos = NP.aceptors.positions
        >>> r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
        >>> np.testing.assert_allclose(r, 15)

        Volumetrical doped

        >>> dopantes_propios = Aceptor(10, 1.3, 'vol')
        >>> dopantes = Aceptor(4, 3.2, 'vol')
        >>> NP = Nanoparticle([15, 0.5], 0.333, 50, 1, dopantes_propios)
        >>> np.random.seed(2)
        >>> NP.doped(dopantes)
        >>> NP.aceptors.positions
        array([[ -9.97994851,  -4.68407978,   2.79838913],
               [ -2.95667238,  -2.5118831 ,  -2.15824574],
               [  2.87360327,  11.94459721,   0.21645999],
               [ -9.23033613,   4.45082408,  -4.92229105]])

        """
        self.aceptors = aceptors
        self.aceptors.generate(self.radio)

    def excite(self, way):
        """
        Generate and exiton inside the NP.

        Parameters
        ----------
        way : str
            Way to exite the NP. Can be 'laser' or 'electro'.

        Examples
        --------

        TODO
        ----
        """
        self.exiton = Exciter(way, self.radio)
