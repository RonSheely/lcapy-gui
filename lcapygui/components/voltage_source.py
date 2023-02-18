from typing import Union
from .component import Component


class VoltageSource(Component):
    """
    VoltageSource

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the voltage source.
    """

    TYPE = "V"
    NAME = "Voltage Source"
    kinds = {'DC': 'dc', 'AC': 'ac', 'Step': 'step', 'Arbitrary': ''}
    can_stretch = True

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)
        self.kind = 'DC'
