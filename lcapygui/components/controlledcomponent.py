from .bipole import Bipole


class ControlledComponent(Bipole):

    @property
    def sketch_net(self):

        return self.type + ' 1 2 3 4'
