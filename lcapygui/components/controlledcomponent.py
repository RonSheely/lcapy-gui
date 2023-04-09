from .component import Component


class ControlledComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.type + ' 1 2 3 4'
