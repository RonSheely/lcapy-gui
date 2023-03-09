from .transistor import Transistor


class FET(Transistor):

    type = "M"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    kinds = {'': '', 'nmos': 'nmos', 'pmos': 'pmos', 'nmosd': 'nmosd', 'pmosd': 'pmosd',
             'nfet': 'nfet', 'pfet': 'pfet', 'nfetd': 'nfetd', 'pfetd': 'pfetd',
             'nigfetd': 'nigfetd', 'pigfetd': 'pigfetd',
             'nigfete': 'nfigete', 'pigfete': 'pigfete',
             'nigfetebulk': 'nigfetebulk', 'pigfetebulk': 'pigfetebulk',
             'hemt': 'hemt'}
