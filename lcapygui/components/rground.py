from .connection import Connection
from numpy import array


class RGround(Connection):
    """
    Rail ground connection
    """

    TYPE = "A"
    NAME = "RGround"

    def __draw_on__(self, editor, layer):

        # Height of stem
        h = 0.3
        # Width of rail
        w = 0.5

        paths = [array(((0, 0), (0, -h))),
                 array(((-w / 2, -h), (w / 2, -h)))]

        spaths = self._tf(paths, 2)
        for path in spaths:
            layer.stroke_path(path)

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, rground'
