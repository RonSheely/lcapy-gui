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
