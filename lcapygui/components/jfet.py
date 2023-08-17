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
    ppins = {'d': ('lx', 0.55, 0),
             'g': ('lx', 0, 0.645),
             's': ('lx', 0.55, 1)}
    npins = {'d': ('lx', 0.55, 1),
             'g': ('lx', 0, 0.355),
             's': ('lx', 0.55, 0)}
    ippins = {'d': ('lx', 0, 0),
              'g': ('lx', 0.55, 0.645),
              's': ('lx', 0, 1)}
    inpins = {'d': ('lx', 0, 1),
              'g': ('lx', 0.55, 0.355),
              's': ('lx', 0, 0)}
