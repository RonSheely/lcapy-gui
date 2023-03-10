from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    kinds = {'': '', 'nigbt': 'nigbt', 'pigbt': 'pigbt', 'Lnigbt': 'Lnigbt',
             'Lpigbt': 'Lpigbt'}

    # TODO: add base offset for Lnigbt, Lpigbt
