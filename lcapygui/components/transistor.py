from .component import Component
from numpy import array, sqrt, dot, degrees
from numpy.linalg import norm
from math import atan2


class Transistor(Component):

    can_stretch = True
    label_offset = 0.6
    has_value = False
    # extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        dx = x1 - x2
        dy = y1 - y2
        r = sqrt(dx**2 + dy**2)
        R = array(((dx, -dy), (dy, dx))) / r

        # Midpoint
        ym = (y1 + y2) / 2
        xm = (x1 + x2) / 2

        # TODO: The offset might change with transistor types.
        # Note, the transistor base/gate is down.
        xg, yg = dot(R, (0, 2))
        xg += xm
        yg += ym

        # D G S
        positions = array(((x1, y1),
                           (xg, yg),
                           (x2, y2)))
        return positions

    @property
    def node1(self):

        return self.nodes[0]

    @property
    def node2(self):

        return self.nodes[2]

    @property
    def sketch_net(self):

        # With up, drain is down.
        s = self.type + ' 1 2 3 ' + self.cpt_kind + '; up'
        if self.symbol_kind != '':
            s += ', kind=' + self.symbol_kind
        return s
