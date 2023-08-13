"""
Defines the components that lcapy-gui can draw
"""

from .tf import TF

from numpy import array, dot, nan
from numpy.linalg import norm
from lcapy.opts import Opts

from typing import Union
from abc import ABC, abstractmethod
from math import sqrt, degrees, atan2


class Component(ABC):

    """
    Describes an lcapy-gui component.
    This is an abstract class, specific components are derived from this.
    """

    args = ('Value', )
    kinds = {}
    styles = {}
    can_stretch = False
    default_kind = ''
    default_style = ''
    label_offset = 0.6
    angle_offset = 0
    # Common fields used for all components
    fields = {'label': 'Label',
              'voltage_label': 'Voltage label',
              'current_label': 'Current label',
              'flow_label': 'Flow label',
              'color': 'Color',
              'scale': 'Scale',
              'attrs': 'Attributes'}
    # Extra fields such as `mirror`, `invert` as used by opamps and transistors
    extra_fields = {}
    has_value = True

    voltage_keys = ('v', 'v_', 'v^', 'v_>', 'v_<', 'v^>', 'v^<',
                    'v<', 'v>')
    current_keys = ('i', 'i_', 'i^', 'i_>',  'i_<', 'i^>', 'i^<',
                    'i>_', 'i<_', 'i>^', 'i<^', 'i>', 'i<', 'ir')
    flow_keys = ('f', 'f_', 'f^', 'f_>',  'f_<', 'f^>', 'f^<',
                 'f>_', 'f<_', 'f>^', 'f<^', 'f>', 'f<')
    label_keys = ('l', 'l_', 'l^')
    annotation_keys = ('a', 'a_', 'a^')

    # These are not passed to the sketcher.
    ignore_keys = ('left', 'right', 'up', 'down', 'size', 'rotate',
                   'pinnodes', 'pinnames', 'pins', 'pinlabels',
                   'mirrorinputs', 'free', 'ignore', 'nosim', 'arrow',
                   'startarrow', 'endarrow', 'bus', 'anchor', 'fixed')

    # TODO: add class methods to construct Component from
    # an Lcapy cpt or from a cpt type.

    def __init__(self, kind='', style='', name=None, nodes=None, opts=None):

        if nodes is None:
            nodes = []
        # opts are the Lcapy drawing attributes such as `right`, `color=blue`.
        # opts is None if the component has been created by the user
        # otherwise it is an Opts object created when the component is
        # loaded from a file.
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
        self.scale = '1'

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

        # Parse the opts and set the component attributes

        # Set mirror and invert attributes
        for k, v in self.extra_fields.items():
            if k in opts:
                opts.remove(k)
                setattr(self, k, True)

        # Remove opts that we don't care about or cannot deal with
        opts = self.filter_opts(opts)

        parts = []
        for k, v in opts.items():
            if k in ('color', 'colour'):
                self.color = v
            elif k == 'scale':
                self.scale = v
            elif k == 'kind':
                self.kind += '-' + v
            elif k == 'style':
                self.style = v
            elif k in self.voltage_keys:
                self.voltage_label = v
            elif k in self.current_keys:
                self.current_label = v
            elif k in self.flow_keys:
                self.flow_label = v
            elif k in self.label_keys:
                self.label = v
            elif k in self.annotation_keys:
                pass
            elif k in self.ignore_keys:
                pass
            else:
                if v == '':
                    parts.append(k)
                else:
                    parts.append(k + '=' + v)

        # attrs is a catch-all for the user-defined attributes that
        # we don't care about.
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

    def _sketch_lookup(self, model):

        ui = model.ui
        style = model.preferences.style

        sketch = ui.sketchlib.lookup(self.sketch_key, style)
        return sketch

    def draw(self, model, **kwargs):
        """
        Handles drawing specific features of components.
        """

        sketch = self._sketch_lookup(model)

        # Handle ports where nothing is drawn.
        if sketch is None:
            return

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        dx = x2 - x1
        dy = y2 - y1

        r = self.length
        if r == 0:
            model.ui.show_warning_dialog(
                'Ignoring zero size component ' + self.name)
            return

        angle = self.angle

        kwargs = self.make_kwargs(model, **kwargs)

        if 'invisible' in kwargs or 'nodraw' in kwargs or 'ignore' in kwargs:
            return

        # Width in cm
        w = sketch.width / 72 * 2.54

        scale = float(self.scale)
        if scale > r / w:
            scale = r / w

        p1 = array((x1, y1))
        if r != 0:
            dw = array((dx, dy)) / r * (r - w * scale) / 2
            p1p = p1 + dw
        else:
            # For zero length wires
            dw = array((0, 0))
            p1p = p1

        sketch.draw_old(model, offset=p1p, angle=angle, scale=scale,
                    snap=True, **kwargs)

        # Add stretchable wires
        if self.can_stretch:

            p2 = array((x2, y2))
            p2p = p2 - dw

            # TODO: generalize
            kwargs.pop('mirror', False)
            kwargs.pop('invert', False)

            sketcher = model.ui.sketcher
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
                h = sketch.height / 72 * 2.54
                dh = array((dx, dy)) / r * (r - h)
                p3p = p3 + dh
                sketcher.stroke_line(*p3, *p3p, **kwargs)

        # TODO, add label, voltage_label, current_label, flow_label

    def _line_width_to_lw(self, model, line_width):
        """Return line width as a float for use with matplotlib."""

        # TODO, handle other units?
        if line_width.endswith('pt'):
            line_width = float(line_width[0:-2])
        elif line_width.endswith('mm'):
            line_width = float(line_width[0:-2]) * 72 / 25.4
        else:
            model.ui.show_warning_dialog('Assuming points for line width')
            line_width = float(line_width)

        return line_width * model.preferences.line_width_scale

    def make_kwargs(self, model, **kwargs):

        opts = Opts(self.attrs)

        line_width = model.preferences.line_width
        lw = self._line_width_to_lw(model, line_width)

        kwargs['lw'] = kwargs.pop('lw', lw)

        for k, v in opts.items():
            if k in ('bodydiode', ):
                continue
            if v == '':
                v = True
            if k == 'line width':
                k = 'lw'
                v = self._line_width_to_lw(model, v)
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
        Returns the length of the component.
        """
        return (self.node2.pos - self.node1.pos).norm()

    @property
    def midpoint(self):
        """
        Returns the midpoint of the component.
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

    def assign_positions1(self, x1, y1, x2, y2, pinname1, pinname2) -> array:

        # Note, this transform will have to change if the component is moved
        tf = self.make_tf(x1, y1, x2, y2, self.pins[pinname1][1:],
                          self.pins[pinname2][1:])

        coords = []
        for node_pinname in self.node_pinnames:
            if node_pinname == '':
                coords.append((nan, nan))
            else:
                coords.append(self.pins[node_pinname][1:])

        positions = tf.transform(coords)

        return positions

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
        """Return Lcapy attribute string such as `right, color=blue`"""

        attr = self.attr_dir_string(x1, y1, x2, y2, step)

        if self.scale != '1':
            attr += ', scale=' + self.scale
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

    @property
    def netitem_args(self):

        if self.cpt_kind == '':
            return ()
        return (self.cpt_kind, )

    def netitem(self, node_names, x1, y1, x2, y2, step=1):
        """Create Lcapy netlist item such as `R1 1 2; right, color=blue`"""

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
        """This is called after a component is created to update
        the nodes and opts."""

        # Defining the nodes on component creation is gnarly and
        # requires the node positions to be passed as arguments.
        if nodes is not None:
            self.nodes = nodes

        # This updates the opts such as `right` that cannot be
        # determined until the node positions are defined.   However,
        # the opts attribute is only used by connection.py and probably
        # should be removed to avoid confusion.
        if opts is not None:
            self.opts = opts

    def choose_node_name(self, m, nodes):

        num = 1
        while True:
            name = str(num)
            if name not in nodes:
                return name
            num += 1

    def make_tf(self, x1, y1, x2, y2, pin1, pin2):

        u0, v0 = pin1
        u1, v1 = pin2

        return TF.from_points_pair((u0, v0), (x1, y1), (u1, v1), (x2, y2))

    def find_tf(self, pinname1, pinname2, node1=None, node2=None):

        if node1 is None:
            node1 = self.node1
        if node2 is None:
            node2 = self.node2

        pin1 = self.pins[pinname1][1:]
        pin2 = self.pins[pinname2][1:]

        return self.make_tf(node1.pos.x, node1.pos.y, node2.pos.x, node2.pos.y,
                            pin1, pin2)
