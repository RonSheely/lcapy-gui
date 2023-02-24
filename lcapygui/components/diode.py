from .component import BipoleComponent


class Diode(BipoleComponent):
    """
    Diode
    """

    TYPE = 'D'
    NAME = 'Diode'
    kinds = {'': '', 'led': 'LED', 'photo': 'Photo', 'schottky': 'Schottky',
             'zener': 'Zener', 'zzener': 'Zzener', 'tunnel': 'Tunnel',
             'varcap': 'VarCap', 'bidirectional': 'Bidirectional',
             'tvs': 'TVS', 'laser': 'Laser'}
    styles = {'empty': 'Empty', 'full': 'Full', 'stroke': 'Stroke'}
    default_kind = ''
    default_style = 'empty'
    schematic_kind = True

    @property
    def sketch_net(self):

        s = self.TYPE + ' 1 2; right'
        if self.kind != '':
            s += ', kind=' + self.kind
        if self.style != '':
            s += ', style=' + self.style
        return s
