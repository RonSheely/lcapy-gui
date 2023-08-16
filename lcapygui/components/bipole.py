from .component import Component


class BipoleComponent(Component):

    can_stretch = True

    node_pinnames = ('+', '-')
    pins = {'+': ('lx', -0.5, 0),
            '-': ('rx', 0.5, 0)}
    pinname1 = '+'
    pinname2 = '-'

    hw = 0.5
    hh = 0.25
    bbox_path = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    @property
    def sketch_net(self):

        s = self.type + ' 1 2; right'
        if self.symbol_kind != '':
            s += ', kind=' + self.symbol_kind
        if self.style != '':
            s += ', style=' + self.style
        return s
