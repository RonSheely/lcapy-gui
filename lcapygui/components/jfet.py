from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    can_stretch = True
    angle_offset = 90
    default_kind = 'njf-'

    kinds = {'njf-': 'NJFET',
             'pjf-': 'PJFET'}

    # TODO: add gate offset
