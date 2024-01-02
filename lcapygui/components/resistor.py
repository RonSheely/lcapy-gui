from .bipole import Bipole


class Resistor(Bipole):

    type = 'R'
    default_kind = ''
    kinds = {'': '', '-variable': 'Variable',
             '-tunable': 'Tunable'}
