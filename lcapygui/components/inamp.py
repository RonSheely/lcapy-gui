from .opamp import Opamp
from .utils import point_in_triangle
from numpy import array, sqrt, nan
from numpy.linalg import norm


class Inamp(Opamp):

    type = "Einamp"
    sketch_net = 'E 1 2 inamp 3 4 5 6'
    sketch_key = 'inamp'
    label_offset = -1
    args = ('Ad', 'Ac', 'Rf')

    node_pinnames = ('out', 'ref', 'in+', 'in-', 'r+', 'r-')

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

    @property
    def pins(self):
        return self.npins if self.mirror else self.ppins

    pinlabels = {'vdd': 'VDD', 'vss': 'VSS'}

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    def netitem_nodes(self, node_names):

        parts = []
        for node_name in node_names[0:2]:
            parts.append(node_name)
        parts.append('inamp')
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
