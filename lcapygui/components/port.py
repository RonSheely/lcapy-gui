from .component import Component


class Port(Component):
    """
    Port
    """

    TYPE = "P"
    NAME = "Port"

    sketch_net = None
