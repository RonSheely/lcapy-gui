from .component import BipoleComponent


class CurrentSource(BipoleComponent):
    """
    CurrentSource

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = 'I'
    NAME = 'Current Source'
    kinds = {'DC': 'dc', 'AC': 'ac', 'Step': 'step', 'Arbitrary': ''}
    default_kind = 'DC'

    @property
    def sketch_net(self):

        # TODO handle arbitrary
        return self.TYPE + ' 1 2 ' + self.kinds[self.kind] + ' ' + '; down'
