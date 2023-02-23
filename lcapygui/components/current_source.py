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
    kinds = {'dc': 'DC', 'ac': 'AC', 'step': 'Step',
             '': 'Arbitrary', 'noise': 'Noise'}
    default_kind = ''

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2 ' + self.kind + ' ' + '; right'
