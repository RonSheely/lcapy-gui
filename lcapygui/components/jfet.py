from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    default_kind = 'njf-'

    kinds = {'njf-': 'NJFET',
             'pjf-': 'PJFET'}

    # TODO: add gate offset

    pinname1 = 's'
    pinname2 = 'd'

    node_pinnames = ('d', 'g', 's')
    ppins = {'d': ('lx', 0.266, -0.5),
             'g': ('lx', -0.2838, 0.145),
             's': ('lx', 0.266, 0.5)}
