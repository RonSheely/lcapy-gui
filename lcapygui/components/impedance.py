from .component import BipoleComponent


class Impedance(BipoleComponent):
    """
    Impedance

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the impedance.
    """

    TYPE = 'Z'
    NAME = 'Impedance'
