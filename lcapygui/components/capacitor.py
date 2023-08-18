from .bipole import Bipole


class Capacitor(Bipole):

    type = 'C'
    default_kind = '-'
    kinds = {'-': '', '-electrolytic': 'Electrolytic',
             '-polar': 'Polar', '-variable': 'Variable',
             '-curved': 'Curved', '-sensor': ' Sensor',
             '-tunable': 'Tunable'}
