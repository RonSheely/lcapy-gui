from .connection import Connection
from .picture import Picture, Multiline


class Ground(Connection):
    """
    Ground connection
    """

    TYPE = "A"
    NAME = "Ground"

    # Height of stem
    h = 0.6
    # Width
    w = 0.8
    # Separation
    s = 0.2

    pic = Picture(Multiline((0, 0), (0, -h)),
                  Multiline((-w / 2, -h), (w / 2, -h)),
                  Multiline((-w / 4, -h - s), (w / 4, -h - s)),
                  Multiline((-w / 8, -h - 2 * s), (w / 8, -h - 2 * s)))

    def draw(self, editor, layer):

        drawer = editor.ui.drawer
        return drawer.draw(self.pic, offset=self.nodes[0].position)

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, ground'
