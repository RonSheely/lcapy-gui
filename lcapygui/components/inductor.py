from .component import BipoleComponent


class Inductor(BipoleComponent):
    """
    Inductor

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the inductor.
    """

    TYPE = 'L'
    NAME = 'Inductor'
    yoffset = -1.4
