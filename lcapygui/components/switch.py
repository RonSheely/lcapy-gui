from .bipole import Bipole


class Switch(Bipole):

    type = 'SW'
    default_kind = ''
    args = ('Time', )
    default_kind = 'no'
    kinds = {'': '', 'nc': 'Normally closed',
             'no': 'Normally open',
             'push': 'Pushbutton'}

    @property
    def sketch_net(self):

        s = self.type + ' 1 2 ' + self.cpt_kind + ' 0; right'
        return s
