from .component import Component
from numpy import array


class Ground(Component):
    """
    Ground Flag
    """

    TYPE = "A"
    NAME = "Ground"

    def __init__(self):

        super().__init__(None)

    @property
    def midpoint(self) -> array:
        """
        Computes the midpoint of the component.
        """

        return array(self.nodes[0].position)

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return 0.5

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), ))

    def _tf(self, paths, scale=1.0):

        newpaths = []
        for path in paths:
            # TODO, rotate
            newpath = path * scale
            newpath = newpath + self.midpoint
            newpaths.append(newpath)
        return newpaths

    def __draw_on__(self, editor, layer):

        paths = [array(((0, 0), (0, -0.2))),
                 array(((-0.2, -0.2), (0.2, -0.2))),
                 array(((-0.1, -0.3), (0.1, -0.3))),
                 array(((-0.05, -0.4), (0.05, -0.4)))]

        spaths = self._tf(paths, 2)
        for path in spaths:
            layer.stroke_path(path)

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, ground'
