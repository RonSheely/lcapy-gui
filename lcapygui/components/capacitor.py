from typing import Union
from .component import Component


class Capacitor(Component):
    """
    Capacitor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the capacitor.
    """

    TYPE = "C"
    NAME = "Capacitor"
    can_stretch = True

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
