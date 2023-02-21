from .connection import Connection


class Ground(Connection):
    """
    Ground connection
    """

    TYPE = "A"
    NAME = "Ground"
    default_kind = 'Ground'

    kinds = {'': '', 'Ground': 'ground', 'Sground': 'sground',
             'Rground': 'rground'}

    @property
    def sketch_net(self):

        return self.TYPE + ' 1' '; down, ' + self.kind

    def net(self, connections, step=1):

        return self.name + ' ' + self.nodes[0].name + '; down, ' \
            + self.kind
