from .component import ControlledComponent


class VCCS(ControlledComponent):
    """
    VCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "G"
    NAME = "VCCS"
