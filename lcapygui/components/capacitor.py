from .component import BipoleComponent


class Capacitor(BipoleComponent):
    """
    Capacitor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the capacitor.
    """

    TYPE = 'C'
    NAME = 'Capacitor'
