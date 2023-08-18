from .bipole import Bipole


class Resistor(Bipole):

    type = 'R'
    label_offset = 0.4
    default_kind = '-'
    kinds = {'-': '', '-variable': 'Variable',
             '-tunable': 'Tunable'}
