from .bipole import Bipole


class Port(Bipole):

    type = "P"
    args = ()
    sketch_net = 'P 1 2'
    has_value = False
