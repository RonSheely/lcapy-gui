from .transistor import Transistor


class MOSFET(Transistor):

    type = "M"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    kinds = {'': '', 'nmos': 'nmos', 'pmos': 'pmos', 'nmosd': 'nmosd', 'pmosd': 'pmosd',
             'nfet': 'nfet', 'pfet': 'pfet',
             'nfet-bodydiode': 'nfet-bodydiode',
             'pfet-bodydiode': 'pfet-bodydiode',
             'nfetd': 'nfetd', 'pfetd': 'pfetd',
             'nfetd-bodydiode': 'nfetd-bodydiode',
             'pfetd-bodydiode': 'pfetd-bodydiode',
             'nigfetd': 'nigfetd', 'pigfetd': 'pigfetd',
             'nigfete': 'nfigete', 'pigfete': 'pigfete',
             'nigfetebulk': 'nigfetebulk', 'pigfetebulk': 'pigfetebulk',
             'hemt': 'hemt'}

    # TODO: add base offset for nigfetd, pigfetd, nigfete, pigfete,
    # nigfetebulk, pigfetebulk

    # TODO support bodydiode
    # Perhaps add new components to Lcapy such as nfet-bodydiode
