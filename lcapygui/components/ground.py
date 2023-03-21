from .connection import Connection


class Ground(Connection):

    type = "W"
    default_kind = '-ground'

    kinds = {'-': '', '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground'}

    @property
    def sketch_net(self):

        return 'W 1 0; down=0, ' + self.kind

    def attr_string(self, step=1):

        return 'down=0, ' + self.kind
