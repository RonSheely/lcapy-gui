from .bipole import Bipole


class Capacitor(Bipole):

    type = 'C'
    default_kind = ''
    kinds = {'': '', '-electrolytic': 'Electrolytic',
             '-polar': 'Polar', '-variable': 'Variable',
             '-curved': 'Curved', '-sensor': ' Sensor',
             '-tunable': 'Tunable'}
    label_offset_pos = (0, -0.5)
    annotation_offset_pos = (0, 0.5)
