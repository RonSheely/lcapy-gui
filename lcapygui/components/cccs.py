from .component import BipoleComponent


class CCCS(BipoleComponent):
    """
    CCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "F"
    NAME = "CCCS"
