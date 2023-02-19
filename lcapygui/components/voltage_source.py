from .component import BipoleComponent


class VoltageSource(BipoleComponent):
    """
    VoltageSource

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the voltage source.
    """

    TYPE = 'V'
    NAME = 'Voltage Source'
    kinds = {'DC': 'dc', 'AC': 'ac', 'Step': 'step', 'Arbitrary': ''}
    default_kind = 'DC'

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2 ' + self.kinds[self.kind] + ' ' + '; right'
