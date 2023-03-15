from .bipole import Component


class Port(Component):

    type = "P"
    args = ()
    sketch_net = 'P 1 2'
    has_value = False
