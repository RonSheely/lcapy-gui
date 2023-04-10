from .component import Component
from numpy import array, sqrt
from numpy.linalg import norm


def point_in_triangle(x, y, x0, y0, x1, y1, x2, y2):

    s = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2)
    t = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)

    if ((s < 0) != (t < 0) and s != 0 and t != 0):
        return False

    d = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)

    return d == 0 or (d < 0) == (s + t <= 0)


class Opamp(Component):

    type = "Eopamp"
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

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        r = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # TODO: handle rotation

        xo = (x2 + x1) / 2 + r * 5 / 2
        yo = (y2 + y1) / 2

        positions = array(((xo, yo),
                           (0, 0),
                           (x1, y1),
                           (x1, y2)))
        return positions

    @property
    def midpoint(self):

        pos = (self.nodes[2].pos + self.nodes[3].pos) * 0.5

        return (self.nodes[0].pos + pos) * 0.5

    @property
    def length(self) -> float:

        pos = (self.nodes[2].pos + self.nodes[3].pos) * 0.5

        diff = (pos - self.nodes[0].pos) * 0.5
        return diff.norm()

    def attr_dir_string(self, x1, y1, x2, y2, step=1):

        # TODO: Handle rotation
        dy = abs(y2 - y1)
        size = dy * 5 / 4

        attr = 'right=%s' % size
        return attr

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.nodes[2].pos.x, self.nodes[2].pos.y
        x2, y2 = self.nodes[3].pos.x, self.nodes[3].pos.y

        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        dy = abs(self.nodes[3].y - self.nodes[2].y)
        size = dy * 5 / 4

        kwargs = self.make_kwargs(editor, **kwargs)

        sketcher.sketch(self.sketch, offset=(xc, yc), angle=0, scale=size / 2.5,
                        **kwargs)

    def netitem_nodes(self, node_names):

        parts = []
        for node_name in node_names[0:2]:
            parts.append(node_name)
        parts.append('opamp')
        for node_name in node_names[2:]:
            parts.append(node_name)
        return parts

    def is_within_bbox(self, x, y):

        x0, y0 = self.nodes[0].pos.x, self.nodes[0].pos.y
        x1, y1 = self.nodes[2].pos.x, self.nodes[2].pos.y
        x2, y2 = self.nodes[3].pos.x, self.nodes[3].pos.y

        # TODO, adjust for actual triangle

        return point_in_triangle(x, y, x0, y0, x1, y1, x2, y2)

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]

    def choose_node_name(self, m, nodes):

        # Handle the special ground node.
        if m == 1:
            return '0'
        return super().choose_node_name(m, nodes)
