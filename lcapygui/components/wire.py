from .component import BipoleComponent


class Wire(BipoleComponent):
    """
    Wire
    """

    TYPE = 'W'
    NAME = 'Wire'
    sketch_net = 'W 1 2'
