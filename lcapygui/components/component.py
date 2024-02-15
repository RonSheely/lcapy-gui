"""
Defines the components that lcapy-gui can draw
"""

from .pos import Pos
from .tf import TF
from .utils import point_in_polygon

from numpy import array, nan
from math import sqrt
from lcapy.opts import Opts

from typing import Union
from abc import ABC, abstractmethod


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
    label_offset_pos = (0, -0.3)
    annotation_offset_pos = (0, 0.3)
    label_alignment = ('center', 'top')
    annotation_alignment = ('center', 'bottom')
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

    def __init__(self, kind="", style="", name=None, nodes=None, opts=None):
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
        self.alabel = ''
        self.voltage_label = ''
        self.current_label = ''
        self.flow_label = ''
        self.color = ''
        # This scales the size of the component but not the distance
        # between the nodes.
        self.scale = '1'

        self.mirror = False
        self.invert = False

        # If the kind starts with a - it is considered an Lcapy
        # component style and is represented by an Lcapy component attribute.
        # Without the - it is represented by an Lcapy component keyword.
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
                self.alabel = v
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

        # This is set by the draw() method
        self.picture = None

        # Items to be shown on right click
        self.menu_items = ["edit_cut", "edit_copy", "edit_paste",
                           "edit_delete", "dropdown_inspect_menu",
                           "inspect_properties"]

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

    @property
    def implicit_nodes(self):

        return []

    def _sketch_lookup(self, model):

        ui = model.ui
        style = model.preferences.style

        sketch = ui.sketchlib.lookup(self.sketch_key, style)
        return sketch

    def draw(self, model, **kwargs):

        raise NotImplementedError('TODO')

    def _line_width_to_lw(self, model, line_width):
        """Return line width as a float for use with matplotlib."""

        if not isinstance(line_width, float):
            # TODO, handle other units?
            if line_width.endswith('pt'):
                line_width = float(line_width[0:-2])
            elif line_width.endswith('mm'):
                line_width = float(line_width[0:-2]) * 72 / 25.4
            else:
                model.ui.show_warning_dialog('Assuming points for line width')
            line_width = float(line_width)

        return line_width * model.preferences.line_width_scale * model.zoom_factor

    def make_kwargs(self, model, **kwargs):
        opts = Opts(self.attrs)

        line_width = model.preferences.line_width
        lw = self._line_width_to_lw(model, line_width)

        kwargs["lw"] = kwargs.pop("lw", lw)

        for k, v in opts.items():
            if k in ('bodydiode', 'bulk'):
                continue
            if v == "":
                v = True
            if k == "line width":
                k = "lw"
                v = self._line_width_to_lw(model, v)
            kwargs[k] = v

        if kwargs.pop("thick", False):
            kwargs["lw"] = kwargs["lw"] * 2

        if self.color != "":
            kwargs["color"] = self.color

        if self.mirror:
            kwargs["mirror"] = True

        if self.invert:
            kwargs["invert"] = True

        if kwargs.pop("dashed", False):
            kwargs["linestyle"] = "--"

        if kwargs.pop("dotted", False):
            kwargs["linestyle"] = ":"

        return kwargs

    @property
    def length(self) -> float:
        """
        Returns the length of the component.
        """
        return self.tf.scale_factor

    @property
    def size(self) -> float:
        """
        Returns the size of the component.
        """
        return self.tf.scale_factor

    @property
    def angle(self) -> float:
        """
        Returns the angle of the component in degrees.
        """

        return -self.tf.angle_deg

    @property
    def midpoint(self):
        return Pos(self.tf.transform((0, 0)))

    @property
    def vertical(self) -> bool:
        """
        Returns true if component essentially vertical.
        """

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        return abs(y2 - y1) > abs(x2 - x1)

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        if len(self.nodes) == 2:
            return array(((x1, y1), (x2, y2)))

        tf = self.make_tf(Pos(x1, y1), Pos(x2, y2), self.pos1, self.pos2)

        coords = []
        for node_pinname in self.node_pinnames:
            if node_pinname == "":
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
    def pos1(self):
        return Pos(self.pins[self.pinname1][1:])

    @property
    def pos2(self):
        return Pos(self.pins[self.pinname2][1:])

    def _attr_dir_string(self, x1, y1, x2, y2, step=1):
        tf = self.make_tf(Pos(x1, y1), Pos(x2, y2), self.pos1, self.pos2)
        r = tf.scale_factor / 2
        angle = -tf.angle_deg + self.angle_offset

        if self.type == "X" and r >= 0.5:
            r -= 0.49

        r = round(r, 2)
        if r == 1:
            size = ""
        else:
            size = "=" + str(r).rstrip("0").rstrip(".")

        angle = round(angle, 2)

        if r == 0:
            attr = "down=0"
            print("Zero length component; this will be drawn down")
        elif angle == 0:
            attr = "right" + size
        elif angle in (90, -270):
            attr = "up" + size
        elif angle in (180, -180):
            attr = "left" + size
        elif angle in (270, -90):
            attr = "down" + size
        else:
            attr = "rotate=" + str(angle).rstrip("0").rstrip(".")

        if r < 1:
            attr += ', scale=' + str(r)

        return attr

    def attr_string(self, x1, y1, x2, y2, step=1):
        """Return Lcapy attribute string such as `right, color=blue`"""

        attr = self._attr_dir_string(x1, y1, x2, y2, step)

        if self.scale != '1':
            attr += ', scale=' + str(self.scale)
        if self.color != '':
            attr += ', color=' + self.color
        # TODO, add cunning way of specifing modifiers, e.g., v^, i<
        if self.voltage_label != '':
            attr += ', v=' + self.voltage_label
        if self.current_label != '':
            attr += ', i=' + self.current_label
        if self.flow_label != '':
            attr += ', f=' + self.flow_label
        if self.label != '':
            attr += ', l=' + self.label
        if self.mirror:
            attr += ", mirror"
        if self.invert:
            attr += ", invert"

        # Add user defined attributes such as thick, dashed, etc.
        if self.attrs != "":
            attr += ", " + self.attrs

        kind = self.symbol_kind
        if kind not in (None, ""):
            if self.type == "W":
                attr += ", " + kind
            else:
                attr += ", kind=" + kind

        if self.style not in (None, ""):
            attr += ", style=" + self.style

        return attr

    def distance_from_cpt(self, x, y):
        """
        Return distance from component to point (x, y).

        Parameters
        ==========
        x : float
            x coordinate of point
        y : float
            y coordinate of point

        Returns
        =======
        float
            Distance from component to point (x, y)
        """
        # Calculate difference between nodes

        if not self.node1.is_drawn or not self.node2.is_drawn:
            return 100

        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        rsq = float(dx**2 + dy**2)

        if rsq == 0.0:
            # Nodes should not be at the same place; this can happen
            # with an opamp ground node that is noot drawn.
            return 100

        # Perform linear interpolation to find closest point on line
        lerp = ((x - self.node1.x) * dx + (y - self.node1.y) * dy) / rsq
        # If the point is outside the line segment, clamp to the nearest node
        if lerp < 0:
            lerp = 0
        elif lerp > 1:
            lerp = 1

        # Convert back to Cartesian coordinates
        new_x = lerp * dx + self.node1.x
        new_y = lerp * dy + self.node1.y
        dx = new_x - x
        dy = new_y - y

        rsq = dx**2 + dy**2
        return sqrt(rsq)

    def is_within_bbox(self, x, y):
        tf = self.tf.inverted()

        xb, yb = tf.transform((x, y))

        path = array(self.bbox_path) * 0.7

        return point_in_polygon(xb, yb, path)

    def netitem_nodes(self, node_names):
        parts = []
        for node_name in node_names:
            parts.append(node_name)
        return parts

    @property
    def netitem_args(self):
        if self.cpt_kind == "":
            return ()
        return (self.cpt_kind,)

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

            if 'scale' in opts:
                self.scale = float(opts['scale'])

    def choose_node_name(self, m, nodes):
        num = 1
        while True:
            name = str(num)
            if name not in nodes:
                return name
            num += 1

    def make_tf(self, p1, p2, q1, q2):
        return TF.from_points_pair(q1.xy, p1.xy, q2.xy, p2.xy)

    def find_tf(self, pinname1, pinname2, node1=None, node2=None):
        if node1 is None:
            node1 = self.node1
        if node2 is None:
            node2 = self.node2

        return self.make_tf(node1.pos, node2.pos, self.pos1, self.pos2)

    @property
    def tf(self):
        # If this was cached then need to update if the node
        # positions are changed.
        tf = self.find_tf(self.pinname1, self.pinname2)

        return tf

    def undraw(self):
        if self.picture is not None:
            self.picture.remove()
        for ann in self.annotations:
            ann.remove()
        self.annotations = []

        # TODO: erase nodes if necessary
        # Could combine annotations with picture

    @property
    def ppins(self):
        raise ValueError("Ppins not defined for %s" % self)

    @property
    def pins(self):
        newpins = {}
        for pinname, data in self.ppins.items():
            loc, x, y = data
            if self.mirror:
                y = -y
            if self.invert:
                x = -x
            newpins[pinname] = loc, x, y
        return newpins
