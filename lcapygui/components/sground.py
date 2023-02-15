from .connection import Connection
from .picture import Picture, Multiline


class SGround(Connection):
    """
    Signal ground connection
    """

    TYPE = "A"
    NAME = "Ground"

    # Height of stem
    h = 0.6
    # Width
    w = 0.6

    pic = Picture(Multiline((0, 0), (0, -h), (w / 2, -h),
                            (0, -2 * h), (-w / 2, -h), (0, -h)))

    def __draw_on__(self, editor, layer):

        drawer = editor.ui.drawer
        return drawer.draw(self.pic, offset=self.nodes[0].position)

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, sground'
