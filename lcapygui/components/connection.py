from .bipole import Bipole
from .picture import Picture
from .tf import TF
from math import cos, sin, radians, sqrt
from numpy import array


class Connection(Bipole):

    # Both Wire and Connection use the W type since Lcapy treats
    # connection as wires.
    type = 'W'
    args = ()
    has_value = False

    kinds = {'-0V': '0V',
             '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground',
             '-vcc': 'VCC', '-vdd': 'VDD', '-vee': 'VEE', '-vss': 'VSS',
             '-input': 'Input', '-output': 'Output', '-bidir': 'Bidirectional'}

    # TODO: fixme
    hw = 0.1
    hh = 0.1
    bbox_path = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    def draw(self, model, **kwargs):

        kwargs = self.make_kwargs(model, **kwargs)
        if 'invisible' in kwargs or 'nodraw' in kwargs or 'ignore' in kwargs:
            return

        sketch = self._sketch_lookup(model)

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        if self.symbol_kind in ('vcc', 'vdd'):
            x1, y1, angle = self.split_node_pos(x2, y2, model, True)
            offset = x1, y1
            angle = angle + 90
        elif self.symbol_kind in ('vee', 'vss'):
            x2, y2, angle = self.split_node_pos(x1, y1, model)
            offset = x2, y2
            angle = angle + 90
        elif self.symbol_kind in ('input', ):
            x2, y2, angle = self.split_node_pos(x1, y1, model)
            offset = x2, y2
        else:
            x2, y2, angle = self.split_node_pos(x1, y1, model)
            offset = x2, y2

        tf = TF().rotate_deg(angle).translate(*offset)
        sketcher = model.ui.sketcher

        self.picture = Picture()
        self.picture.add(sketch.draw(model, tf, **kwargs))
        self.picture.add(sketcher.stroke_line(x1, y1, x2, y2, **kwargs))

    def split_node_pos(self, x, y, model, flip=False):

        step = model.preferences.node_spacing

        # TODO, generate opts as needed.
        # attr = self.attr_string(
        # self.node1.x, self.node1.y, self.node2.x, self.node2.y, step)
        #
        # from lcapy.opts import Opts
        # opts = Opts(attr)

        opts = self.opts

        def get_value(direction):

            val = opts[direction]
            if val == '':
                value = 1
            else:
                value = float(val)

            return value * step

        scale = -1 if flip else 1

        # TODO fix if positive node unknown, say for vdd, vcc.

        if 'down' in opts:
            angle = -90
            y -= get_value('down') * scale
        elif 'up' in opts:
            angle = 90
            y += get_value('up') * scale
        elif 'right' in opts:
            angle = 0
            x += get_value('right') * scale
        elif 'left' in opts:
            angle = 180
            x -= get_value('left') * scale
        elif 'angle' in opts:
            angle = get_value('angle')
            if 'size' in opts:
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

    @property
    def implicit_nodes(self):

        if self.symbol_kind == '':
            return []
        return [self.nodes[1]]

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
