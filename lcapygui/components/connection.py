from .bipole import BipoleComponent
from math import cos, sin, radians, sqrt
from numpy import array


class Connection(BipoleComponent):

    type = 'X'
    args = ()
    has_value = False

    kinds = {'-0V': '0V',
             '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground',
             '-vcc': 'VCC', '-vdd': 'VDD', '-vee': 'VEE', '-vss': 'VSS',
             '-input': 'Input', '-output': 'Output', '-bidir': 'Bidirectional'}

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(editor, **kwargs)

        if self.symbol_kind in ('vcc', 'vdd'):
            x1, y1, angle = self.split_node_pos(x2, y2, editor.STEP, True)
            offset = x1, y1
            angle = angle + 90
        elif self.symbol_kind in ('vee', 'vss'):
            x2, y2, angle = self.split_node_pos(x1, y1, editor.STEP)
            offset = x2, y2
            angle = angle + 90
        elif self.symbol_kind in ('input', ):
            x2, y2, angle = self.split_node_pos(x1, y1, editor.STEP)
            offset = x2, y2
        else:
            x2, y2, angle = self.split_node_pos(x1, y1, editor.STEP)
            offset = x2, y2

        sketcher.sketch(self.sketch, offset=offset,
                        angle=angle, snap=False, **kwargs)

        sketcher.stroke_line(x1, y1, x2, y2, **kwargs)

    def split_node_pos(self, x, y, step=1, flip=False):

        def get_value(direction):

            val = self.opts[direction]
            if val == '':
                value = 1
            else:
                value = float(val)

            return value * step

        scale = -1 if flip else 1

        # TODO fix if positive node unknown, say for vdd, vcc.

        if 'down' in self.opts:
            angle = -90
            y -= get_value('down') * scale
        elif 'up' in self.opts:
            angle = 90
            y += get_value('up') * scale
        elif 'right' in self.opts:
            angle = 0
            x += get_value('right') * scale
        elif 'left' in self.opts:
            angle = 180
            x -= get_value('left') * scale
        elif 'angle' in self.opts:
            angle = get_value('angle')
            if 'size' in self.opts:
                size = get_value('size')
            else:
                size = 1
            x += size * cos(radians(angle))
            y += size * sin(radians(angle))
        else:
            # Assume right
            x += 1
            angle = 0

        return x, y, angle

    @property
    def sketch_net(self):

        return 'W 1 0; right=0, ' + self.symbol_kind + ', l='

    @property
    def labelled_nodes(self):

        if self.symbol_kind == '':
            return self.nodes
        elif self.symbol_kind in ('vcc', 'vdd'):
            return self.nodes[1:]
        else:
            return self.nodes[:1]

    @property
    def drawn_nodes(self):

        if self.symbol_kind == '':
            return self.nodes
        elif self.symbol_kind in ('vcc', 'vdd'):
            return self.nodes[1:]
        else:
            return self.nodes[:1]

    def is_within_bbox(self, x, y):

        # FIXME
        xm = self.midpoint.x
        ym = self.midpoint.y

        r = sqrt((x - xm)**2 + (y - ym)**2)
        return r < 0.5

    def choose_node_name(self, m, nodes):

        if m == 0 and self.symbol_kind in ('vcc', 'vdd'):
            return self.symbol_kind

        if m == 1 and self.symbol_kind in ('vee', 'vss', '0V', 'ground',
                                           'rground', 'sground', 'cground'):
            return '0'

        return super().choose_node_name(m, nodes)
