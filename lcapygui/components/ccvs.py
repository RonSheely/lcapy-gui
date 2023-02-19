
import numpy as np

from typing import Union

from .component import Component


class CCVS(Component):
    """
    CCVS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the CCVS.
    """

    TYPE = "H"
    NAME = "CCVS"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
