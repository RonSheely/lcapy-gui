from .transistor import Transistor
from lcapy.cache import cached_property


class MOSFET(Transistor):

    type = "M"
    default_kind = 'nmos-nfet'

    kinds = {'nmos-nmos': 'NMOS simple',
             'pmos-pmos': 'PMOS simple',
             'nmos-nmosd': 'NMOS depletion',
             'pmos-pmosd': 'PMOS depletion',
             'nmos-nfet': 'NMOS enhancement',
             'pmos-pfet': 'PMOS enhancement',
             'nmos-nfet-bodydiode': 'NMOS enhancement with body diode',
             'pmos-pfet-bodydiode': 'PMOS enhancement with body diode',
             'nmos-nfetd': 'NMOS depletion',
             'pmos-pfetd': 'PMOS depletion',
             'nmos-nfetd-bodydiode': 'NMOS depletion with body diode',
             'pmos-pfetd-bodydiode': 'PMOS depletion with body diode',
             'nmos-nigfetd': 'NMOS insulated gate depletion',
             'pmos-pigfetd': 'PMOS insulated gate depletion',
             'nmos-nigfetd-bodydiode': 'NMOS insulated gate depletion with bodydiode',
             'pmos-pigfetd-bodydiode': 'PMOS insulated gate depletion with bodydiode',
             'nmos-nigfete': 'NMOS insulated gate enhancement',
             'pmos-pigfete': 'PNMOS insulated gate enhancement',
             'nmos-nigfete-bodydiode': 'NMOS insulated gate enhancement with body diode',
             'pmos-pigfete-bodydiode': 'PMOS insulated gate enhancement with body diode',
             # 'nmos-nigfetebulk': 'nigfetebulk',
             # 'nmos-pigfetebulk': 'pigfetebulk',
             '-hemt': 'HEMT'}

    # TODO: add base offset for nigfetd, pigfetd, nigfete, pigfete,
    # nigfetebulk, pigfetebulk

    node_pinnames = ('d', 'g', 's')

    mos_pins = {'d': ('lx', 0.2661, 0.5),
                'g': ('lx', -0.2874, 0),
                's': ('lx', 0.2661, -0.5)}
    igfet_pins = {'d': ('lx', 0.2661, 0.5),
                  'g': ('lx', -0.2891, -0.145),
                  's': ('lx', 0.2661, -0.5)}
    body_diode_pins = {'d': ('lx', 0.154, 0.5),
                       'g': ('lx', -0.396, 0),
                       's': ('lx', 0.154, -0.5)}

    @property
    def is_igfet(self):
        return 'igfet' in self.kind

    @property
    def has_body_diode(self):
        return 'bodydiode' in self.kind

    @property
    def pinname1(self):
        return 's' if self.is_ptype else 'd'

    @property
    def pinname2(self):
        return 'd' if self.is_ptype else 's'

    @cached_property
    def ppins(self):
        # What about igfet with bodydiode?

        if self.is_igfet:
            return self.igfet_pins
        elif self.has_body_diode:
            return self.body_diode_pins
        else:
            return self.mos_pins

    @property
    def label_offset_pos(self):

        if self.has_body_diode:
            return (0.8, 0)
        else:
            return (0.6, 0)
