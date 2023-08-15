from .opamp import Opamp
from .utils import point_in_triangle
from numpy import array, sqrt
from numpy.linalg import norm

# Grrr, why is this different in size to an opamp in Circutikz?
# It has a length of 2.2 compared to 2 for an opamp.


class FDOpamp(Opamp):

    type = "Efdopamp"
    sketch_net = 'E 1 2 fdopamp 3 4 5'
    sketch_key = 'fdopamp'
    label_offset = -1
    args = ('Ad', 'Ac', 'Ro')

    node_pinnames = ('out+', 'out-', 'in+', 'in-', 'ocm')

    ppins = {'out+': ('r', 0.85, -0.5),
             'out-': ('r', 0.85, 0.5),
             'in+': ('l', -1.25, 0.5),
             'ocm': ('l', -0.85, 0),
             'in-': ('l', -1.25, -0.5),
             'vdd': ('t', -0.25, 0.645),
             'vss': ('b', -0.25, -0.645),
             'r+': ('l', -0.85, 0.25),
             'r-': ('l', -0.85, -0.25)}

    npins = {'out-': ('r', 0.85, -0.5),
             'out+': ('r', 0.85, 0.5),
             'in-': ('l', -1.25, 0.5),
             'ocm': ('l', -0.85, 0),
             'in+': ('l', -1.25, -0.5),
             'vdd': ('t', -0.25, 0.645),
             'vss': ('b', -0.25, -0.645),
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
        parts.append('fdopamp')
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
