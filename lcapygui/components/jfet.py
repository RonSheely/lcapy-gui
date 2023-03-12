from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    angle_offset = 90
    default_kind = 'njf-'

    kinds = {'njf-': 'NJFET',
             'pjf-': 'PJFET'}

    # TODO: add gate offset
