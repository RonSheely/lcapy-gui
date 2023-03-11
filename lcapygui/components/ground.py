from .connection import Connection


class Ground(Connection):

    type = "A"
    default_kind = '-ground'

    kinds = {'-': '', '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground'}

    @property
    def sketch_net(self):

        return self.type + ' 1' '; down, ' + self.kind

    def attr_string(self, step=1):

        return 'down, ' + self.kind
