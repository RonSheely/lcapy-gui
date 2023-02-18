from typing import Union
from .component import Component


class Resistor(Component):
    """
    Resistor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the resistor.
    """

    TYPE = "R"
    NAME = "Resistor"
    can_stretch = True

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
