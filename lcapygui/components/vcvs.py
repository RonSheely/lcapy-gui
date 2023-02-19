
import numpy as np

from typing import Union

from .component import BipoleComponent


class VCVS(BipoleComponent):
    """
    VCVS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the VCVS.
    """

    TYPE = "E"
    NAME = "VCVS"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
