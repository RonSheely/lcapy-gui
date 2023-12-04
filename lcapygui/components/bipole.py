from .stretchy import Stretchy
from numpy import array


class Bipole(Stretchy):

    node_pinnames = ('+', '-')
    ppins = {'+': ('lx', -0.5, 0),
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

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), (x2, y2)))
