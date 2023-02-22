from .connection import Connection


class SGround(Connection):
    """
    Signal ground connection
    """

    TYPE = "A"
    NAME = "Ground"

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, sground'
