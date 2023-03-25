from .bipole import BipoleComponent


class Wire(BipoleComponent):

    type = 'W'
    args = ()
    has_value = False
    default_kind = '-'

    kinds = {'-': '', '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground',
             '-vcc': 'VCC', '-vdd': 'VDD', '-vee': 'VEE', '-vss': 'VSS'}

    connection_keys = ('input', 'output', 'bidir', 'pad')
    ground_keys = ('ground', 'sground', 'rground',
                   'cground', 'nground', 'pground', '0V')
    supply_positive_keys = ('vcc', 'vdd')
    supply_negative_keys = ('vee', 'vss')
    supply_keys = supply_positive_keys + supply_negative_keys
    implicit_keys = ('implicit', ) + ground_keys + supply_keys

    def filter_opts(self, opts):

        stripped = list(opts.strip(*self.implicit_keys))
        if len(stripped) > 1:
            raise ValueError('Multiple wire kinds: ' + ', '.join(stripped))
        elif len(stripped) == 1:
            kind = stripped[0]
            if kind == 'implicit':
                kind = 'ground'
            self.kind = kind
        return opts

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(editor, **kwargs)
        sketcher.stroke_line(x1, y1, x2, y2, **kwargs)

        if self.symbol_kind != '':

            if self.symbol_kind in ('vcc', 'vdd'):
                offset = x1, y1
                angle = self.angle + 90
            elif self.symbol_kind in ('vee', 'vss'):
                offset = x2, y2
                angle = self.angle + 90
            else:
                offset = x2, y2
                angle = self.angle

            # TODO, draw vcc, vdd on positive node.
            sketcher.sketch(self.sketch, offset=offset,
                            angle=angle, snap=False, **kwargs)

    @property
    def sketch_net(self):

        return 'W 1 0; right=0, ' + self.symbol_kind

    @property
    def label_nodes(self):

        if self.symbol_kind == '':
            return self.nodes
        elif self.symbol_kind in ('vcc', 'vdd'):
            return self.nodes[1:]
        else:
            return self.nodes[:1]
