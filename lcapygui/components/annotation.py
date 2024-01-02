from .connection import Connection


class Annotation(Connection):

    type = "A"
    args = ()
    default_kind = '-ground'
    angle_offset = 90

    kinds = {'': '', '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground',
             '-vcc': 'VCC', '-vdd': 'VDD', '-vee': 'VEE', '-vss': 'VSS',
             '-input': 'Input', '-output': 'Output', '-bidir': 'Bidirectional'}

    @property
    def sketch_net(self):

        return 'A 0; right, ' + self.symbol_kind

    def attr_string(self, x1, y1, x2, y2, step=1):

        return self.symbol_kind
