from .component import BipoleComponent


class Admittance(BipoleComponent):
    """
    Admittance

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the admittance.
    """

    TYPE = 'Y'
    NAME = 'Admittance'
