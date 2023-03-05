from .component import Component
from numpy import array, sqrt
from numpy.linalg import norm


class Opamp(Component):

    type = "E"
    sketch_net = 'E 1 2 opamp 3 4'
    sketch_key = 'opamp'
    label_offset = 0
    args = ('Ad', 'Ac', 'Ro')

    # The Nm node is not used (ground).
    node_pinnames = ('out', '', 'in+', 'in-')

    ppins = {'out': ('rx', 1.25, 0.0),
             'in+': ('lx', -1.25, 0.5),
             'in-': ('lx', -1.25, -0.5),
             'vdd': ('t', 0, 0.5),
             'vdd2': ('t', -0.45, 0.755),
             'vss2': ('b', -0.45, -0.755),
             'vss': ('b', 0, -0.5),
             'ref': ('b', 0.45, -0.245),
             'r+': ('l', -0.85, 0.25),
             'r-': ('l', -0.85, -0.25)}

    npins = {'out': ('rx', 1.25, 0.0),
             'in-': ('lx', -1.25, 0.5),
             'in+': ('lx', -1.25, -0.5),
             'vdd': ('t', 0, 0.5),
             'vdd2': ('t', -0.45, 0.755),
             'vss2': ('b', -0.45, -0.755),
             'vss': ('b', 0, -0.5),
             'ref': ('b', 0.45, -0.245),
             'r-': ('l', -0.85, 0.25),
             'r+': ('l', -0.85, -0.25)}

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        r = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # TODO: handle rotation

        xo = (x2 + x1) / 2
        yo = r * 4 / 5

        positions = array(((xo, yo),
                           (0, 0),
                           (x1, y1),
                           (x1, y2)))
        return positions

    @property
    def midpoint(self):

        pos = (self.nodes[2].pos + self.nodes[3].pos) * 0.5

        return (self.nodes[0].pos + pos) * 0.5

    def length(self) -> float:

        pos = (self.nodes[2].pos + self.nodes[3].pos) * 0.5

        diff = (pos - self.nodes[0].pos) * 0.5
        return diff.norm()

    def attr_string(self, step=1):

        # TODO: Handle rotation
        dy = abs(self.nodes[3].y - self.nodes[2].y)
        size = dy * 5 / 4

        attr = 'right=%s' % size

        # Add user defined attributes such as color=blue, thick, etc.
        if self.attrs != '':
            attr += ', ' + self.attrs

        return attr

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.nodes[2].pos.x, self.nodes[2].pos.y
        x2, y2 = self.nodes[3].pos.x, self.nodes[3].pos.y

        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        dy = abs(self.nodes[3].y - self.nodes[2].y)
        size = dy * 5 / 4

        kwargs = self.make_kwargs(editor, **kwargs)

        if 'mirror' in kwargs:
            kwargs.pop('mirror')
            print('TODO: add mirror')

        if 'invert' in kwargs:
            kwargs.pop('invert')
            print('TODO: add invert')

        sketcher.sketch(self.sketch, offset=(xc, yc), angle=0, scale=size / 2.5,
                     **kwargs)
