from .component import BipoleComponent


class Diode(BipoleComponent):
    """
    Diode
    """

    TYPE = 'D'
    NAME = 'Diode'
    kinds = {'': '', 'LED': 'led', 'Zener': 'zener'}
    default_kind = ''

    @property
    def sketch_net(self):

        kind = self.kinds[self.kind]
        s = self.TYPE + ' 1 2; down'
        if kind != '':
            s += ', kind=' + kind
        return s
