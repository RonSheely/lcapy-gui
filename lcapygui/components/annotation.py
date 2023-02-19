from .connection import Connection


class Annotation(Connection):
    """
    Ground connection
    """

    TYPE = "A"
    NAME = "Ground"

    kinds = {'Ground': 'ground', 'Sground': 'sground', 'Rground': 'rground'}

    def __init__(self, kind='Ground'):

        super().__init__()
        self.kind = kind

    @property
    def sketch_net(self):

        return self.TYPE + ' 1' '; down, ' + self.kinds[self.kind]

    def net(self, connections, step=1):

        # TODO: make vdd go up
        return self.name + ' ' + self.nodes[0].name + '; down, ' \
            + self.kinds[self.kind]
