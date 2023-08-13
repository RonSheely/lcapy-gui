from .component import Component
from .utils import point_in_triangle
from numpy import array, sqrt
from numpy.linalg import norm

# Grrr, why is this different in size to an opamp in Circutikz?
# It has a length of 2.2 compared to 2 for an opamp.


class FDOpamp(Component):

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

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        return self.assign_positions1(x1, y1, x2, y2, 'in+', 'in-')

    @property
    def midpoint(self):

        return (self.nodes[0].pos + self.nodes[1].pos +
                self.nodes[2].pos + self.nodes[3].pos) * 0.25

    @property
    def length(self) -> float:

        # FIXME

        pos = (self.nodes[2].pos + self.nodes[3].pos) * 0.5

        diff = (pos - self.nodes[0].pos) * 0.5
        return diff.norm()

    def attr_dir_string(self, x1, y1, x2, y2, step=1):

        # TODO: Handle rotation
        dy = abs(y2 - y1)
        size = dy / 2

        attr = 'right=%s' % size
        return attr

    def draw(self, model, **kwargs):

        sketch = self._sketch_lookup(model)

        x1, y1 = self.nodes[2].pos.x, self.nodes[2].pos.y
        x2, y2 = self.nodes[3].pos.x, self.nodes[3].pos.y

        xc = (x1 + x2) / 2
        yc = (y1 + y2) / 2

        dy = abs(self.nodes[3].y - self.nodes[2].y)
        size = dy * 5 / 4

        kwargs = self.make_kwargs(model, **kwargs)

        sketch.draw(model, offset=(xc, yc), angle=0, scale=size / 2.5,
                    **kwargs)

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
