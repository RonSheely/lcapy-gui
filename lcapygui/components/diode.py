from .component import BipoleComponent


class Diode(BipoleComponent):
    """
    Diode
    """

    TYPE = 'D'
    NAME = 'Diode'
    kinds = {'': '', 'led': 'LED', 'zener': 'Zener'}
    default_kind = ''
    schematic_kind = True

    @property
    def sketch_net(self):

        kind = self.kind
        s = self.TYPE + ' 1 2; right'
        if kind != '':
            s += ', kind=' + kind
        return s
