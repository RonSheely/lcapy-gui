from typing import Union
from .component import BipoleComponent


class VCCS(BipoleComponent):
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
