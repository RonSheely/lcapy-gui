from .component import Component


class BipoleComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        s = self.type + ' 1 2; right'
        if self.symbol_kind != '':
            s += ', kind=' + self.symbol_kind
        return s
