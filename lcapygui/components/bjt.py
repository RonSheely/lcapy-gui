from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    kinds = {'': '', 'nigbt': 'nigbt', 'pigbt': 'pigbt', 'Lnigbt': 'Lnigbt',
             'Lpigbt': 'Lpigbt'}
