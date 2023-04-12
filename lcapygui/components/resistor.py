from .bipole import BipoleComponent


class Resistor(BipoleComponent):

    type = 'R'
    label_offset = 0.4
    default_kind = '-'
    kinds = {'-': '', '-variable': 'Variable',
             '-tunable': 'Tunable'}
