from .transistor import Transistor


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

    pinname1 = 's'
    pinname2 = 'd'

    node_pinnames = ('d', 'g', 's')
    ppins1 = {'d': ('lx', 0.2661, 0.5),
              'g': ('lx', -0.2874, 0),
              's': ('lx', 0.2661, -0.5)}
    ppins2 = {'d': ('lx', 0.2661, 0.5),
              'g': ('lx', -0.2891, -0.145),
              's': ('lx', 0.2661, -0.5)}

    @property
    def ppins(self):

        if (self.style is not None
            and (self.style.startswith('pigfet')
                 or self.style.startswith('nigfet'))):
            return self.ppins2
        else:
            return self.ppins1
