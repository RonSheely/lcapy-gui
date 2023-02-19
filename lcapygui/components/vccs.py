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
