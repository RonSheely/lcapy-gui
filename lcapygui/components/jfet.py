from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    default_kind = 'njf'

    kinds = {'njf': 'NJFET',
             'pjf': 'PJFET'}

    # TODO: add gate offset

    node_pinnames = ('d', 'g', 's')
    njf_pins = {'d': ('lx', 0.266, 0.5),
                'g': ('lx', -0.2838, -0.145),
                's': ('lx', 0.266, -0.5)}
    pjf_pins = {'d': ('lx', 0.266, -0.5),
                'g': ('lx', -0.2838, 0.145),
                's': ('lx', 0.266, 0.5)}

    @property
    def pinname1(self):
        return 'd' if self.is_ntype else 's'

    @property
    def pinname2(self):
        return 's' if self.is_ntype else 'd'

    @property
    def pins(self):

        return self.njf_pins if self.is_ntype else self.pjf_pins
