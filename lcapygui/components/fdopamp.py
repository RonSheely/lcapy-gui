from .opamp import Opamp
from numpy import array, sqrt
from numpy.linalg import norm

# Grrr, why is this different in size to an opamp in Circutikz?
# It has a length of 2.2 compared to 2 for an opamp.


class FDOpamp(Opamp):

    type = "Efdopamp"
    sketch_net = 'E 1 2 fdopamp 3 4 5'
    sketch_key = 'fdopamp'
    label_offset_pos = (0, -1)
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

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]
