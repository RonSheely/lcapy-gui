from typing import Union
from .component import Component
from numpy import array, sqrt
from numpy.linalg import norm


class Opamp(Component):
    """
    Opamp

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the opamp.
    """

    TYPE = "E"
    NAME = "Opamp"

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

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)

    def _tf(self, path, scale=1.0):

        # TODO, rotate
        path = path * self.length() / scale * 2
        path = path + self.midpoint
        return path

    def draw(self, editor, layer):

        path = array(((-0.85, -1), (-0.85, 1), (.85, 0),
                     (-0.85, -1)), dtype=float)

        wire_in_plus = array(((-1.25, 0.5), (-0.85, 0.5)))
        wire_in_minus = array(((-1.25, -0.5), (-0.85, -0.5)))
        wire_out = array(((0.85, 0), (1.25, 0)))

        s = 2.5
        path = self._tf(path, s)

        wire_in_plus = self._tf(wire_in_plus, s)
        wire_in_minus = self._tf(wire_in_minus, s)
        wire_out = self._tf(wire_out, s)

        plus = self._tf(array((-0.7, 0.5)), s)
        minus = self._tf(array((-0.7, -0.5)), s)

        layer.stroke_polygon(path)

        layer.stroke_line(wire_in_plus[0, 0], wire_in_plus[0, 1],
                          wire_in_plus[1, 0], wire_in_plus[1, 1])

        layer.stroke_line(wire_in_minus[0, 0], wire_in_minus[0, 1],
                          wire_in_minus[1, 0], wire_in_minus[1, 1])

        layer.stroke_line(wire_out[0, 0], wire_out[0, 1],
                          wire_out[1, 0], wire_out[1, 1])

        layer.text(plus[0], plus[1], '+', fontsize=20, ha='center')
        layer.text(minus[0], minus[1], '-', fontsize=20, ha='center')

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        length = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # TODO: handle rotation
        positions = array(((x2, y2),
                           (0, 0),
                           (x1, y2 + length / 5),
                           (x1, y2 - length / 5)))
        return positions

    @property
    def midpoint(self) -> float:

        pos = (self.nodes[2].position + self.nodes[3].position) / 2

        return (self.nodes[0].position + pos) / 2

    def length(self) -> float:

        pos = (self.nodes[2].position + self.nodes[3].position) / 2

        diff = (pos - self.nodes[0].position) / 2
        return norm(diff)
