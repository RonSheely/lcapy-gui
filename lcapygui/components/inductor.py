from .bipole import BipoleComponent


class Inductor(BipoleComponent):

    type = 'L'
    default_kind = '-'
    kinds = {'-': '', '-variable': 'Variable', '-choke': 'Choke',
             '-twolineschoke': 'Two lines choke',
             '-sensor': 'Sensor', '-tunable': 'Tunable'}
