from .bipole import Bipole


class VoltageSource(Bipole):

    type = 'V'
    kinds = {'dc': 'DC', 'ac': 'AC', 'step': 'Step',
             '': 'Arbitrary', 'noise': 'Noise', 's': ''}
    default_kind = ''
    label_offset_pos = (0, -0.5)
    annotation_offset_pos = (0, 0.5)

    @property
    def sketch_net(self):

        return self.type + ' 1 2 ' + self.kind + ' ' + '; right'
