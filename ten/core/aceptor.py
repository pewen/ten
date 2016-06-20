"""
Aceptor Object
"""

from __future__ import division, absolute_import, print_function

from ..utils.extMath import random_points_in_sphere


class Aceptor(object):
    """
    Create aceptors.
    """

    def __init__(self, number, r_mechanisms, way):
        """
        Inialize N aceptors.

        Parameters
        ----------
        number : int
            Number of aceptors.
        r_mechanisms : float
            Radio usado en el macanismo de transfrencia.
            [r_mechanisms] = nm.
        way : str
            Can by 'sup' to generate in the surface or 'vol'.


        Returns
        -------
        out : Aceptor object

        Raises
        ------
        ValueError
            if way diferent of 'sup' or 'vol'.


        Examples
        --------
        >>> aceptors = Aceptor(10, 1.3, 'sup')
        >>> aceptors.number
        10

        >>> aceptors = Aceptor(10, 1.3, 'sup')
        >>> aceptors.way
        'sup'

        >>> aceptors = Aceptor(10, 1.3, 'vol')
        >>> aceptors.r_mechanisms
        1.3

        >>> aceptors = Aceptor(10, 1.3, 'volum')
        Traceback (most recent call last):
            ...
        ValueError: 'way' must be 'sup', 'superficial', 'vol' or 'volumetrical'

        """
        posible_way = ['sup', 'superficial', 'vol', 'volumetrical']
        if way not in posible_way:
            raise ValueError("'way' must be 'sup', 'superficial'," +
                             " 'vol' or 'volumetrical'")

        self.number = number
        self.r_mechanisms = r_mechanisms
        self.way = way
        self.position = []

    def generate(self, radio):
        """
        Genera la posicion de los N aceptores dentro de la NP
        dependiendo de la forma en la que se crearon.

        Parameters
        ----------
        radio : float
            NP radio.


        Examples
        --------
        Check genaration in the sup.

        >>> import numpy as np
        >>> NP_radio = 15
        >>> aceptors = Aceptor(10, 1.3, 'sup')
        >>> aceptors.generate(NP_radio)
        >>> pos = aceptors.position
        >>> r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
        >>> np.testing.assert_allclose(r, NP_radio)

        Check generated in the volume.

        >>> aceptors = Aceptor(10, 1.3, 'vol')
        >>> aceptors.generate(NP_radio)
        >>> pos = aceptors.position
        >>> r = np.sqrt(pos[:, 0]**2 + pos[:, 1]**2 + pos[:, 2]**2)
        >>> all(r <= NP_radio) and all(r > 0)
        True

        TODO
        ----
        - Hoy se considera que los acceptores son un punto.
          Darle realidad física y chequear que no se superpongan.
        """
        if self.way in ['sup', 'superficial']:
            second_radio = radio
        else:
            second_radio = 0

        self.position = random_points_in_sphere(self.number,
                                                radio,
                                                second_radio)
