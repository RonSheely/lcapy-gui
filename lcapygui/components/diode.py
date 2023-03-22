from .bipole import BipoleComponent


class Diode(BipoleComponent):

    type = 'D'
    args = ()
    kinds = {'-': '', '-led': 'LED', '-photo': 'Photo', '-schottky': 'Schottky',
             '-zener': 'Zener', '-zzener': 'Zzener', '-tunnel': 'Tunnel',
             '-varcap': 'VarCap', '-bidirectional': 'Bidirectional',
             '-tvs': 'TVS', '-laser': 'Laser'}
    styles = {'empty': 'Empty', 'full': 'Full', 'stroke': 'Stroke'}
    default_kind = '-'
    default_style = 'empty'
    has_value = False

    @property
    def sketch_net(self):

        s = self.type + ' 1 2; right'
        if self.symbol_kind != '':
            s += ', kind=' + self.symbol_kind
        if self.style != '':
            s += ', style=' + self.style
        return s
