from .fixed import Fixed

from numpy import array


# TODO: make stretchy


# There is a lot more to do to support transformers.  Tapped
# transformers have 6 nodes.  The user may want to select the input
# port, the output port, or the entire device.


class Transformer(Fixed):

    type = "TF"
    default_kind = ''

    kinds = {'': 'Default',
             'core': 'With core',
             # The taps require extra nodes...
             #   'tap': 'Center tapped',
             #   'tapcore': 'Center tapped with core'
             }
    pinname1 = 'p+'
    pinname2 = 'p-'

    node_pinnames = ('s+', 's-', 'p+', 'p-')

    hw = 0.32
    # Actual half-height
    # hh = 0.48245
    hh = 0.5
    ppins = {'s+': ('rx', hw, hh),
             's-': ('rx', hw, -hh),
             'p+': ('lx', -hw, hh),
             'p-': ('lx', -hw, -hh)}

    bbox_path = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]

    def is_within_bbox(self, x, y):

        # TODO: handle rotation, see component.py
        w = abs(self.nodes[2].x - self.nodes[0].x)
        h = abs(self.nodes[0].y - self.nodes[1].y)

        midpoint = self.midpoint

        x -= midpoint.x
        y -= midpoint.y

        # TODO: perhaps select input or output pair of nodes
        return x > -w / 2 and x < w / 2 and y > -h / 2 and y < h / 2

    @property
    def sketch_net(self):

        return 'TF 1 2 3 4 ' + self.kind

    @property
    def label_position(self):
        """
        Returns position where to place label.
        """

        # -0.2 is the centre for length == 1.

        pos = self.midpoint
        w = self.label_offset * self.length
        if self.vertical:
            pos.x += w
        else:
            pos.y += w

        return pos
