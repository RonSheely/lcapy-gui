from .component import BipoleComponent


class Diode(BipoleComponent):
    """
    Diode
    """

    TYPE = "R"
    NAME = "Diode"

    def __init__(self):

        super().__init__(None)
