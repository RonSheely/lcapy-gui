from .bipole import Bipole


class Diode(Bipole):

    type = 'D'
    args = ()
    kinds = {'': '', '-led': 'LED', '-photo': 'Photo', '-schottky': 'Schottky',
             '-zener': 'Zener', '-zzener': 'Zzener', '-tunnel': 'Tunnel',
             '-varcap': 'VarCap', '-bidirectional': 'Bidirectional',
             '-tvs': 'TVS', '-laser': 'Laser'}
    styles = {'empty': 'Empty', 'full': 'Full', 'stroke': 'Stroke'}
    default_kind = ''
    default_style = 'empty'
    has_value = False
