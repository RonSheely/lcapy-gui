from .component import Component
from numpy import array, sqrt, dot, degrees
from numpy.linalg import norm
from math import atan2


class Transistor(Component):

    schematic_kind = True

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

        xg, yg = dot(R.T, (0, -2))
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
        s = self.type + ' 1 2 3; up'
        if self.kind != '':
            s += ', kind=' + self.kind
        return s
