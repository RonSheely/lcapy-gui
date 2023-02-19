
import numpy as np

from typing import Union

from .component import Component


class VCCS(Component):
    """
    VCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "G"
    NAME = "VCCS"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
