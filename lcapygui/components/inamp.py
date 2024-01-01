from .opamp import Opamp
from numpy import array, sqrt, nan
from numpy.linalg import norm


class Inamp(Opamp):

    type = "Einamp"
    sketch_net = 'E 1 2 inamp 3 4 5 6'
    sketch_key = 'inamp'
    label_offset_pos = (0, -1)
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

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]
