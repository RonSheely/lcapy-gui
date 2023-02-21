from .component import ControlledComponent


class CCCS(ControlledComponent):
    """
    CCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "F"
    NAME = "CCCS"
