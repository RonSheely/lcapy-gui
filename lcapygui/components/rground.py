from .connection import Connection
from .picture import Picture, Multiline


class RGround(Connection):
    """
    Rail ground connection
    """

    TYPE = "A"
    NAME = "RGround"

    # Height of stem
    h = 0.6
    # Width of rail
    w = 1

    pic = Picture(Multiline((0, 0), (0, -h)),
                  Multiline((-w / 2, -h), (w / 2, -h)))

    def __draw_on__(self, editor, layer):

        drawer = editor.ui.drawer
        return drawer.draw(self.pic, offset=self.nodes[0].position)

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, rground'
