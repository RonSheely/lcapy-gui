from .component import Component


class BipoleComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.type + ' 1 2'
