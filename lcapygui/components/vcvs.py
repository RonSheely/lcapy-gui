from .component import ControlledComponent


class VCVS(ControlledComponent):
    """
    VCVS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the VCVS.
    """

    TYPE = "E"
    NAME = "VCVS"
