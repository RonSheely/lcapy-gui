from .component import Component
from numpy import array
from lcapy.schemmisc import Pos


# There is a lot more to do to support transformers.  Tapped
# transformers have 6 nodes.  The user may want to select the input
# port, the output port, or the entire device.


class Transformer(Component):

    type = "TF"
    sketch_net = 'TF 1 2 3 4'
    default_kind = 'TF'
    # TODO: probably need a yoffset
    # -0.2 is the centre
    label_offset = 1

    kinds = {'TF': 'Default',
             'TFcore': 'With core',
             'TFtap': 'Center tapped',
             'TFtapcore': 'Center tapped with core'}

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        # TODO: handle rotation
        dy = y1 - y2
        dx = 0.5 * dy
        x3 = x1 + dx
        y3 = y1
        x4 = x2 + dx
        y4 = y2

        positions = array(((x3, y3),
                           (x4, y4),
                           (x1, y1),
                           (x2, y2)))
        return positions

    def attr_dir_string(self, x1, y1, x2, y2, step=1):

        # TODO: Handle rotation
        size = abs(y2 - y1)

        attr = 'right=%s' % size
        return attr

    def draw(self, model, **kwargs):

        sketch = self._sketch_lookup(model)

        # TODO: handle rotation

        x1, y1 = self.nodes[0].pos.x, self.nodes[0].pos.y
        x4, y4 = self.nodes[3].pos.x, self.nodes[3].pos.y

        size = abs(y1 - y4)

        xc = (x1 + x4) / 2
        yc = (y1 + y4) / 2

        kwargs = self.make_kwargs(model, **kwargs)

        sketch.draw(model, offset=(xc, yc), angle=0,
                    scale=size / model.STEP, **kwargs)

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]

    @property
    def midpoint(self):
        """
        Computes the midpoint of the component.
        """

        x = array([node.x for node in self.nodes])
        y = array([node.y for node in self.nodes])

        return Pos(x.mean(), y.mean())

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

        return self.kind + ' 1 2 3 4'
