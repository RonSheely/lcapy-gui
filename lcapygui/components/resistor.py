from .component import BipoleComponent


class Resistor(BipoleComponent):
    """
    Resistor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the resistor.
    """

    TYPE = 'R'
    NAME = 'Resistor'
