from .connection import Connection


class Annotation(Connection):
    """
    Ground connection
    """

    TYPE = 'A'
    NAME = 'Ground'
    default_kind = 'ground'

    kinds = {'': '', 'ground': 'Ground', 'sground': 'Signal ground',
             'rground': 'Rail ground', 'cground': 'Chassis ground'}

    @property
    def sketch_net(self):

        return self.TYPE + ' 1' '; down, ' + self.kind

    def net(self, connections, step=1):

        # TODO: make vdd go up
        return self.name + ' ' + self.nodes[0].name + '; down, ' \
            + self.kind
