from .bipole import BipoleComponent


class Capacitor(BipoleComponent):

    type = 'C'
    default_kind = '-'
    kinds = {'-': '', '-electrolytic': 'Electrolytic',
             '-polar': 'Polar', '-variable': 'Variable',
             '-curved': 'Curved', '-sensor': ' Sensor',
             '-tunable': 'Tunable'}
