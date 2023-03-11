from .transistor import Transistor


class MOSFET(Transistor):

    type = "M"
    can_stretch = True
    angle_offset = 90
    default_kind = 'nmos-nfet'

    kinds = {'nmos-nmos': 'NMOS simple',
             'pmos-pmos': 'PMOS simple',
             'nmos-nmosd': 'NMOS depletion',
             'pmos-pmosd': 'PMOS depletion',
             'nmos-nfet': 'NMOS enhancement',
             'pmos-pfet': 'PMOS enhancement',
             'nmos-nfet-bodydiode': 'NMOS enhancement with bodydiode',
             'pmos-pfet-bodydiode': 'PMOS enhancement with bodydiode',
             'nmos-nfetd': 'NMOS depletion',
             'pmos-pfetd': 'PMOS depletion',
             'nmos-nfetd-bodydiode': 'NMOS depletion with bodydiode',
             'pmos-pfetd-bodydiode': 'PMOS depletion with bodydiode',
             'nmos-nigfetd': 'NMOS insulated gate depletion',
             'pmos-pigfetd': 'PMOS insulated gate depletion',
             'nmos-nigfete': 'NMOS insulated gate enhancement',
             'pmos-pigfete': 'PNMOS insulated gate enhancement',
             # 'nmos-nigfetebulk': 'nigfetebulk',
             # 'nmos-pigfetebulk': 'pigfetebulk',
             '-hemt': 'HEMT'}

    # TODO: add base offset for nigfetd, pigfetd, nigfete, pigfete,
    # nigfetebulk, pigfetebulk
