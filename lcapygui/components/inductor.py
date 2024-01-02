from .bipole import Bipole


class Inductor(Bipole):

    type = 'L'
    default_kind = ''
    kinds = {'': '', '-variable': 'Variable', '-choke': 'Choke',
             '-twolineschoke': 'Two lines choke',
             '-sensor': 'Sensor', '-tunable': 'Tunable'}
    label_offset_pos = (0, -0.2)
