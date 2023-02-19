from .connection import Connection


class Ground(Connection):
    """
    Ground connection
    """

    TYPE = "A"
    NAME = "Ground"

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, ground'
