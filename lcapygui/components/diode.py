from .component import Component


class Diode(Component):
    """
    Diode
    """

    TYPE = "R"
    NAME = "Diode"
    can_stretch = True

    def __init__(self):

        super().__init__(None)
