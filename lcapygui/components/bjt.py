from .transistor import Transistor
from numpy import array, sqrt, dot, degrees
from numpy.linalg import norm
from math import atan2


class BJT(Transistor):

    type = "Q"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    kinds = {'': '', 'nigbt': 'nigbt', 'pigbt': 'pigbt', 'Lnigbt': 'Lnigbt',
             'Lpigbt': 'Lpigbt'}
