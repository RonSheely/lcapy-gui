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
    ppins = {'d': ('lx', 0.55, 0),
             'g': ('lx', 0, 0.5),
             's': ('lx', 0.55, 1)}
    npins = {'d': ('lx', 0.55, 1),
             'g': ('lx', 0, 0.5),
             's': ('lx', 0.55, 0)}
    ippins = {'d': ('lx', 0, 0),
              'g': ('lx', 0.55, 0.5),
              's': ('lx', 0, 1)}
    inpins = {'d': ('lx', 0, 1),
              'g': ('lx', 0.55, 0.5),
              's': ('lx', 0, 0)}
    ppins2 = {'d': ('lx', 0.55, 0),
              'g': ('lx', 0, 0.645),
              's': ('lx', 0.55, 1)}
    npins2 = {'d': ('lx', 0.55, 1),
              'g': ('lx', 0, 0.355),
              's': ('lx', 0.55, 0)}
    ippins2 = {'d': ('lx', 0, 0),
               'g': ('lx', 0.55, 0.645),
               's': ('lx', 0, 1)}
    inpins2 = {'d': ('lx', 0, 1),
               'g': ('lx', 0.55, 0.355),
               's': ('lx', 0, 0)}
