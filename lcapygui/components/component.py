"""
Defines the components that lcapy-gui can draw
"""

from numpy import array, dot
from numpy.linalg import norm
from lcapy.opts import Opts

from typing import Union
from abc import ABC, abstractmethod
from math import sqrt, degrees, atan2


class Component(ABC):

    """
    Describes an lcapy-gui component.
    This is an abstract class, specific components are derived from here.
    """

    args = ('Value', )
    kinds = {}
    styles = {}
    can_stretch = False
    default_kind = ''
    default_style = ''
    label_offset = 0.6
    angle_offset = 0
    fields = {'label': 'Label',
              'voltage_label': 'Voltage label',
              'current_label': 'Current label',
              'flow_label': 'Flow label',
              'color': 'Color',
              'attrs': 'Attributes'}
    extra_fields = {}
    has_value = True
    netitem_args = ()

    # TODO: add class methods to construct Component from
    # an Lcapy cpt or from a cpt type.

    def __init__(self, kind='', style='', name=None, nodes=None, opts=None):

        if nodes is None:
            nodes = []
        if opts is None:
            opts = Opts()
        else:
            opts = opts.copy()

        self.name = name
        self.nodes = nodes
        self.opts = opts
        self.control = None
        self.attrs = ''
        self.annotations = []
        self.label = ''
        self.voltage_label = ''
        self.current_label = ''
        self.flow_label = ''
        self.color = ''
        self.scale = 1

        self.mirror = False
        self.invert = False

        if kind == '':
            kind = self.default_kind
        self.kind = kind
        self.inv_kinds = {v: k for k, v in self.kinds.items()}

        if style == '':
            style = self.default_style
        self.style = style
        self.inv_styles = {v: k for k, v in self.styles.items()}

        for k, v in self.extra_fields.items():
            if k in opts:
                opts.remove(k)
                setattr(self, k, True)

        opts = self.filter_opts(opts)

        parts = []
        for k, v in opts.items():
            if k in ('color', 'colour'):
                self.color = v
            elif k == 'scale':
                try:
                    self.scale = float(v)
                except:
                    self.scale = 1.0
            elif k == 'mirror':
                self.mirror = True
            elif k == 'invert':
                self.invert = True
            elif k == 'kind':
                self.kind = '-' + v
            elif k == 'style':
                self.style = v
            elif k in ('f', 'i', 'v'):
                # TODO, handle labels.
                pass
            elif k in ('left', 'right', 'up', 'down', 'size', 'rotate',
                       'pinnodes', 'pinnames', 'pins', 'pinlabels',
                       'mirrorinputs'):
                pass
            else:
                if v == '':
                    parts.append(k)
                else:
                    parts.append(k + '=' + v)
        self.attrs = ', '.join(parts)

    def filter_opts(self, opts):

        connection_keys = ('input', 'output', 'bidir', 'pad')
        ground_keys = ('ground', 'sground', 'rground',
                       'cground', 'nground', 'pground', '0V')
        supply_positive_keys = ('vcc', 'vdd')
        supply_negative_keys = ('vee', 'vss')
        io_keys = ('input', 'output', 'bidir')
        supply_keys = supply_positive_keys + supply_negative_keys
        implicit_keys = ('implicit', ) + ground_keys + supply_keys + io_keys

        stripped = list(opts.strip(*implicit_keys))
        if len(stripped) > 1:
            raise ValueError('Multiple connection kinds: ' +
                             ', '.join(stripped))
        elif len(stripped) == 1:
            kind = stripped[0]
            if kind == 'implicit':
                kind = 'ground'
            self.kind = '-' + kind

        return opts

    @property
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """
        Component type identifer used by lcapy.
        E.g. Resistors have the identifier R.
        """
        ...

    def __str__(self) -> str:

        return self.type + ' ' + '(%s, %s) (%s, %s)' % \
            (self.node1.pos.x, self.node1.pos.y,
             self.node2.pos.x, self.node2.pos.y)

    @property
    def sketch_key(self):

        s = self.type
        s += '-' + self.cpt_kind
        s += '-' + self.symbol_kind
        s += '-' + self.style
        s = s.strip('-')
        return s

    @property
    def cpt_kind(self):

        parts = self.kind.split('-')
        return parts[0]

    @property
    def symbol_kind(self):

        parts = self.kind.split('-')
        return '-'.join(parts[1:])

    @property
    def labelled_nodes(self):

        return self.nodes

    @property
    def drawn_nodes(self):

        return self.nodes

    def draw(self, editor, sketcher, **kwargs):
        """
        Handles drawing specific features of components.
        """

        # Handle ports where nothing is drawn.
        if self.sketch is None:
            return

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        dx = x2 - x1
        dy = y2 - y1

        r = self.length
        if r == 0:
            editor.ui.show_warning_dialog(
                'Ignoring zero size component ' + self.name)
            return

        angle = self.angle

        # Width in cm
        w = self.sketch.width / 72 * 2.54

        p1 = array((x1, y1))
        if r != 0:
            dw = array((dx, dy)) / r * (r - w) / 2
            p1p = p1 + dw
        else:
            # For zero length wires
            p1p = p1

        kwargs = self.make_kwargs(editor, **kwargs)

        if 'invisible' in kwargs or 'nodraw' in kwargs or 'ignore' in kwargs:
            return

        sketcher.sketch(self.sketch, offset=p1p, angle=angle,
                        snap=True, **kwargs)

        # Add stretchable wires
        if self.can_stretch:

            p2 = array((x2, y2))
            p2p = p2 - dw

            # TODO: generalize
            kwargs.pop('mirror', False)
            kwargs.pop('invert', False)

            sketcher.stroke_line(*p1, *p1p, **kwargs)
            sketcher.stroke_line(*p2p, *p2, **kwargs)

            # For transistors.
            if len(self.nodes) == 3:

                x3, y3 = self.nodes[1].x, self.nodes[1].y

                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                dx = mx - x3
                dy = my - y3
                r = sqrt(dx**2 + dy**2)

                p3 = array((x3, y3))

                # Height in cm
                h = self.sketch.height / 72 * 2.54
                dh = array((dx, dy)) / r * (r - h)
                p3p = p3 + dh
                sketcher.stroke_line(*p3, *p3p, **kwargs)

        # TODO, add label, voltage_label, current_label, flow_label

    def make_kwargs(self, editor, **kwargs):

        opts = Opts(self.attrs)

        kwargs['lw'] = kwargs.pop('lw', editor.preferences.lw)

        for k, v in opts.items():
            if k in ('bodydiode', ):
                continue
            if v == '':
                v = True
            kwargs[k] = v

        if kwargs.pop('thick', False):
            kwargs['lw'] = kwargs['lw'] * 2

        if self.color != '':
            kwargs['color'] = self.color

        if self.mirror:
            kwargs['mirror'] = True

        if self.invert:
            kwargs['invert'] = True

        if kwargs.pop('dashed', False):
            kwargs['linestyle'] = '--'

        if kwargs.pop('dotted', False):
            kwargs['linestyle'] = ':'

        return kwargs

    @property
    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return (self.node2.pos - self.node1.pos).norm()

    @property
    def midpoint(self):
        """
        Computes the midpoint of the component.
        """

        return (self.node1.pos + self.node2.pos) * 0.5

    @property
    def vertical(self) -> bool:
        """
        Returns true if component essentially vertical.
        """

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        return abs(y2 - y1) > abs(x2 - x1)

    @property
    def label_position(self):
        """
        Returns position where to place label.
        """

        pos = self.midpoint
        w = self.label_offset
        if self.vertical:
            pos.x += w
        else:
            pos.y += w

        return pos

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), (x2, y2)))

    @property
    def node1(self):

        return self.nodes[0]

    @property
    def node2(self):

        return self.nodes[1]

    @property
    def angle(self):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        angle = degrees(atan2(y2 - y1, x2 - x1))
        return angle

    def attr_dir_string(self, x1, y1, x2, y2, step=1):

        r = sqrt((x1 - x2)**2 + (y1 - y2)**2) / step

        if self.type == 'X' and r >= 0.5:
            r -= 0.49

        if r == 1:
            size = ''
        else:
            size = '=' + str(round(r, 2)).rstrip('0').rstrip('.')

        angle = degrees(atan2(y2 - y1, x2 - x1)) + self.angle_offset

        if r == 0:
            attr = 'down=0'
            print('Zero length component; this will be drawn down')
        elif angle == 0:
            attr = 'right' + size
        elif angle in (90, -270):
            attr = 'up' + size
        elif angle in (180, -180):
            attr = 'left' + size
        elif angle in (270, -90):
            attr = 'down' + size
        else:
            attr = 'rotate=' + str(round(angle, 2)).rstrip('0').rstrip('.')

        return attr

    def attr_string(self, x1, y1, x2, y2, step=1):

        attr = self.attr_dir_string(x1, y1, x2, y2, step)

        if self.color != '':
            attr += ', color=' + self.color
        # TODO, add cunning way of specifing modifiers, e.g., v^, i<
        if self.voltage_label != '':
            attr += ', v=' + self.voltage_label
        if self.current_label != '':
            attr += ', i=' + self.current_label
        if self.flow_label != '':
            attr += ', f=' + self.flow_label
        if self.mirror:
            attr += ', mirror'
        if self.invert:
            attr += ', invert'

        # Add user defined attributes such as thick, dashed, etc.
        if self.attrs != '':
            attr += ', ' + self.attrs

        kind = self.symbol_kind
        if kind not in (None, ''):
            if self.type == 'X':
                attr += ', ' + kind
            else:
                attr += ', kind=' + kind

        if self.style not in (None, ''):
            attr += ', style=' + self.style

        return attr

    def attr_string_update(self, step=1):

        return self.attr_string(self.node1.x, self.node1.y,
                                self.node2.x, self.node2.y, step=step)

    def is_within_bbox(self, x, y):

        m = array((self.midpoint.x, self.midpoint.y))

        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        r = sqrt(dx**2 + dy**2)

        if r == 0:
            r = 0.3

        R = array(((dx, -dy), (dy, dx))) / r

        # Transform point into non-rotated box
        p = array((x, y))
        q = dot(R.T, (p - m))

        l = self.length - 0.3
        h = 0.3
        x, y = q

        # Determine if transformed point is in the box
        return x > -l / 2 and x < l / 2 and y > -h / 2 and y < h / 2

    def netitem_nodes(self, node_names):

        parts = []
        for node_name in node_names:
            parts.append(node_name)
        return parts

    def netitem(self, node_names, x1, y1, x2, y2, step=1):

        parts = [self.name]
        parts.extend(self.netitem_nodes(node_names))
        if self.type in ('E', 'G'):
            # Need to use known nodes to start with.
            parts.extend([node_names[0], node_names[1]])
        else:
            parts.extend(self.netitem_args)
        netitem = ' '.join(parts)
        attr_string = self.attr_string(x1, y1, x2, y2, step)
        netitem += '; ' + attr_string + '\n'
        return netitem

    def update(self, opts=None, nodes=None):

        if nodes is not None:
            self.nodes = nodes

        if opts is not None:
            self.opts = opts

    def choose_node_name(self, m, nodes):

        num = 1
        while True:
            name = str(num)
            if name not in nodes:
                return name
            num += 1
