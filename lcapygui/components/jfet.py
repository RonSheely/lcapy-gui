from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    default_kind = 'njf'

    kinds = {'njf': 'NJFET',
             'pjf': 'PJFET'}

    # TODO: add gate offset

    node_pinnames = ('d', 'g', 's')
    ppins = {'d': ('lx', 0.266, 0.5),
             'g': ('lx', -0.2838, -0.145),
             's': ('lx', 0.266, -0.5)}

    @property
    def pinname1(self):
        return 's' if self.is_ptype else 'd'

    @property
    def pinname2(self):
        return 'd' if self.is_ptype else 's'
