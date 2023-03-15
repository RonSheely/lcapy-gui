from .component import Component
from numpy import array
from math import sqrt


class Connection(Component):

    def __str__(self) -> str:

        return self.type + ' ' + '(%s, %s)' % \
            (self.nodes[0].pos[0], self.nodes[0].pos[1])

    @property
    def midpoint(self) -> array:
        """
        Computes the midpoint of the component.
        """

        return self.nodes[0].pos + array((0, -0.5))

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return 0.5

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), ))

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.pos.x, self.node1.pos.y

        kwargs = self.make_kwargs(editor, **kwargs)

        sketcher.sketch(self.sketch, offset=(x1, y1), angle=180,
                        **kwargs)

    def is_within_bbox(self, x, y):

        xm = self.midpoint.x
        ym = self.midpoint.y

        r = sqrt((x - xm)**2 + (y - ym)**2)
        return r < 0.5
