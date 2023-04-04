from .bipole import BipoleComponent
from math import cos, sin, radians


class Wire(BipoleComponent):

    type = 'W'
    args = ()
    has_value = False
    default_kind = '-'

    kinds = {'-': '', '-ground': 'Ground', '-sground': 'Signal ground',
             '-rground': 'Rail ground', '-cground': 'Chassis ground',
             '-vcc': 'VCC', '-vdd': 'VDD', '-vee': 'VEE', '-vss': 'VSS'}

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(editor, **kwargs)

        # Handle implicit wires
        if self.symbol_kind != '':

            x2, y2, angle = self.split_node_pos()

            if self.symbol_kind in ('vcc', 'vdd'):
                offset = x1, y1
                angle = angle + 90
            elif self.symbol_kind in ('vee', 'vss'):
                offset = x2, y2
                angle = angle + 90
            else:
                offset = x2, y2
                angle = angle

            # TODO, draw vcc, vdd on positive node.
            sketcher.sketch(self.sketch, offset=offset,
                            angle=angle, snap=False, **kwargs)
        sketcher.stroke_line(x1, y1, x2, y2, **kwargs)

    def split_node_pos(self):

        x2 = self.node1.x
        y2 = self.node1.y

        def get_value(direction):

            val = self.opts[direction]
            if val == '':
                return 1
            return float(val)

        if 'down' in self.opts:
            angle = -90
            y2 += get_value('down')
        elif 'up' in self.opts:
            angle = 90
            y2 -= get_value('up')
        elif 'right' in self.opts:
            angle = 0
            x2 += get_value('right')
        elif 'left' in self.opts:
            angle = 180
            x2 -= get_value('left')
        elif 'angle' in self.opts:
            angle = get_value('angle')
            if 'size' in self.opts:
                size = get_value('size')
            else:
                size = 1
            x2 += size * cos(radians(angle))
            y2 += size * sin(radians(angle))
        else:
            # Assume right
            x2 += 1
            angle = 0

        return x2, y2, angle

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
