from .bipole import BipoleComponent


class Wire(BipoleComponent):

    type = 'W'
    args = ()
    sketch_net = 'W 1 2'
    has_value = False

    connection_keys = ('input', 'output', 'bidir', 'pad')
    ground_keys = ('ground', 'sground', 'rground',
                   'cground', 'nground', 'pground', '0V')
    supply_positive_keys = ('vcc', 'vdd')
    supply_negative_keys = ('vee', 'vss')
    supply_keys = supply_positive_keys + supply_negative_keys
    implicit_keys = ('implicit', ) + ground_keys + supply_keys

    def filter_opts(self, opts):

        stripped = opts.strip(*self.implicit_keys)
        return opts

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(editor, **kwargs)
        sketcher.stroke_line(x1, y1, x2, y2, **kwargs)
