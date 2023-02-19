
import numpy as np

from typing import Union

from .component import Component


class CCCS(Component):
    """
    CCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "F"
    NAME = "CCCS"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
