from typing import Union
from .component import BipoleComponent


class Capacitor(BipoleComponent):
    """
    Capacitor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the capacitor.
    """

    TYPE = "C"
    NAME = "Capacitor"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
