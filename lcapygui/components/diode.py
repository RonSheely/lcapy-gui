from .component import BipoleComponent


class Diode(BipoleComponent):
    """
    Diode
    """

    TYPE = 'R'
    NAME = 'Diode'
    kinds = {'': '', 'LED': 'led', 'Zener': 'zener'}
    default_kind = ''

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2; down, kind=' + self.kinds[self.kind]
