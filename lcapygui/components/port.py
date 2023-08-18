from .bipole import Bipole


class Port(Bipole):

    type = "P"
    args = ()
    sketch_net = 'P 1 2'
    has_value = False
    # A lie but it avoids the wires
    can_stretch = False
