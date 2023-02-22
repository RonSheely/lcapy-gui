from .connection import Connection


class RGround(Connection):
    """
    Rail ground connection
    """

    TYPE = "A"
    NAME = "RGround"

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, rground'
