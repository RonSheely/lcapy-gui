from typing import Union
from .component import BipoleComponent


class CurrentSource(BipoleComponent):
    """
    CurrentSource

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "I"
    NAME = "Current Source"
    kinds = {'DC': 'dc', 'AC': 'ac', 'Step': 'step', 'Arbitrary': ''}
    can_stretch = True

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
        self.kind = 'DC'
