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
             'nmos-nigfetebulk': 'NMOS insulated gate enhancement (bulk)',
             'pmos-pigfetebulk': 'PMOS insulated gate enhancement (bulk)',
             '-hemt': 'HEMT'}

    # TODO: add base offset for nigfetd, pigfetd, nigfete, pigfete,
    # nigfetebulk, pigfetebulk

    node_pinnames = ('d', 'g', 's')

    nmos_pins = {'d': ('lx', 0.2626, 0.5),
                 'g': ('lx', -0.2874, 0),
                 's': ('lx', 0.2626, -0.5)}
    nigfet_pins = {'d': ('lx', 0.2626, 0.5),
                   'g': ('lx', -0.2891, -0.145),
                   's': ('lx', 0.2626, -0.5)}
    nmos_bodydiode_pins = {'d': ('lx', 0.154, 0.5),
                           'g': ('lx', -0.396, 0),
                           's': ('lx', 0.154, -0.5)}
    nigfet_bodydiode_pins = {'d': ('lx', 0.154, 0.5),
                             'g': ('lx', -0.396, -0.145),
                             's': ('lx', 0.154, -0.5)}

    pmos_pins = {'d': ('lx', 0.2626, -0.5),
                 'g': ('lx', -0.2874, 0),
                 's': ('lx', 0.2626, 0.5)}
    pigfet_pins = {'d': ('lx', 0.2626, -0.5),
                   'g': ('lx', -0.2891, -0.145),
                   's': ('lx', 0.2626, 0.5)}
    pmos_bodydiode_pins = {'d': ('lx', 0.154, -0.5),
                           'g': ('lx', -0.396, 0),
                           's': ('lx', 0.154, 0.5)}
    pigfet_bodydiode_pins = {'d': ('lx', 0.154, -0.5),
                             'g': ('lx', -0.396, -0.145),
                             's': ('lx', 0.154, 0.5)}

    @property
    def is_igfet(self):
        return 'igfet' in self.kind

    @property
    def has_bodydiode(self):
        return 'bodydiode' in self.kind

    @property
    def pinname1(self):
        return 's' if self.is_ptype else 'd'

    @property
    def pinname2(self):
        return 'd' if self.is_ptype else 's'

    @cached_property
    def ppins(self):
        if self.is_igfet:
            if self.has_bodydiode:
                return self.nigfet_bodydiode_pins if self.is_ntype else self.pigfet_bodydiode_pins
            else:
                return self.nigfet_pins if self.is_ntype else self.pigfet_pins
        else:
            if self.has_bodydiode:
                return self.nmos_bodydiode_pins if self.is_ntype else self.pmos_bodydiode_pins
            else:
                return self.nmos_pins if self.is_ntype else self.pmos_pins

    @property
    def label_offset_pos(self):

        if self.has_bodydiode:
            return (0.8, 0)
        else:
            return (0.6, 0)

    def __init__(self, kind='', style='', name=None, nodes=None, opts=None):

        if kind == '' and (opts is not None and 'kind' in opts):
            kind = 'nmos' if opts['kind'].startswith('n') else 'pmos'

        super(MOSFET, self).__init__(kind, style, name, nodes, opts)

        if self.kind == 'nmos':
            self.kind = 'nmos-nmos'
        elif self.kind == 'pmos':
            self.kind = 'pmos-pmos'
