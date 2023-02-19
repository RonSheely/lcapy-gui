from typing import Union
from .component import BipoleComponent


class CCVS(BipoleComponent):
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
