from ..components.component import Component
from ..annotation import Annotation
from ..annotations import Annotations
from ..nodes import Nodes
from ..components.components import Components
from .preferences import Preferences
from ..components.cpt_maker import cpt_make
from copy import copy
from numpy import array
from math import atan2, degrees
from lcapy.mnacpts import Eopamp


class UIModelBase:

    STEP = 2
    SNAP = 1
    SCALE = 0.25

    component_map = {
        'c': ('Capacitor', 'C', ''),
        'd': ('Diode', 'D', ''),
        'i': ('Current source', 'I', ''),
        'l': ('Inductor', 'L', ''),
        'r': ('Resistor', 'R', ''),
        'nr': ('Resistor', 'R', ''),
        'v': ('Voltage source', 'V', ''),
        'w': ('Wire', 'W', ''),
        'e': ('VCVS', 'E', ''),
        'f': ('CCCS', 'F', ''),
        'g': ('VCCS', 'G', ''),
        'h': ('CCVS', 'H', ''),
        'opamp': ('Opamp', 'Opamp', ''),
        'p': ('Port', 'P', ''),
        'y': ('Admittance', 'Y', ''),
        'z': ('Impedance', 'Z', ''),
    }

    connection_map = {
        '0': ('0V', 'Ground', ''),
        '0V': ('0V', 'Ground', '0V'),
        'ground': ('Ground', 'Ground', ''),
        'sground': ('Signal ground', 'Ground', 'sground'),
        'rground': ('Rail ground', 'Ground', 'rground'),
        'cground': ('Chassis ground', 'Ground', 'cground'),
        # 'vdd': ('VDD', 'A', 'vdd'),
        # 'vss': ('VSS', 'A', 'vss'),
        # 'input': ('Input', 'A', 'input'),
        # 'output': ('Output', 'A', 'output'),
        # 'bidir': ('Bidirectional', 'A', 'bidir')
    }

    def __init__(self, ui):

        self.components = Components()
        self.nodes = Nodes()
        self.ui = ui
        self._cct = None
        self.filename = ''
        self.voltage_annotations = Annotations()
        self.selected = None
        self.last_expr = None
        self.preferences = Preferences()
        self.dirty = False
        self.history = []
        self.clipped = None

    @property
    def cct(self):

        if self._cct is not None:
            return self._cct

        from lcapy import Circuit

        if len(self.components) == 0:
            self.exception('No circuit defined')
            return None

        try:
            sch = self.components.as_sch(self.STEP)
        except Exception as e:
            self.exception(e)
            return None

        if self.ground_node is None:
            # Add dummy ground node
            sch += 'W %s 0\n' % self.nodes[0].name

        self._cct = Circuit(sch)

        try:
            self._cct[0]
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)
            return None

        return self._cct

    def annotation_make(self, elt, kind=''):

        opts = elt.opts

        for k, v in self.connection_map.items():
            if k in opts:
                return self.con_make(k, kind)
        return None

    def bounding_box(self):

        if len(self.nodes) == 0:
            return None

        xmin = 1000
        xmax = 0
        ymin = 1000
        ymax = 0
        for node in self.nodes:
            if node.x < xmin:
                xmin = node.x
            if node.x > xmax:
                xmax = node.x
            if node.y < ymin:
                ymin = node.y
            if node.y > ymax:
                ymax = node.y
        return xmin, ymin, xmax, ymax

    def con_create(self, con_key, x1, y1, x2, y2):
        """Make and place a connection."""

        cpt = self.con_make(con_key)
        if cpt is None:
            self.exception('Unimplemented connection ' + con_key)
            return
        self.cpt_place(cpt, x1, y1, x2, y2)

    def con_make(self, con_key, kind=''):

        try:
            cpt_class_name = self.connection_map[con_key][1]
            if kind == '':
                kind = self.connection_map[con_key][2]
        except KeyError:
            return None

        if cpt_class_name == '':
            return None

        cpt = cpt_make(cpt_class_name, kind)
        self.invalidate()
        return cpt

    @property
    def cpt_selected(self):

        return isinstance(self.selected, Component)

    def cpt_create(self, cpt_key, x1, y1, x2, y2):
        """Make and place a component."""

        cpt = self.cpt_make(cpt_key)
        if cpt is None:
            self.exception('Unimplemented component ' + cpt_key)
            return
        self.cpt_place(cpt, x1, y1, x2, y2)

    def cpt_delete(self, cpt):

        self.select(None)

        redraw = True
        try:
            # This should also delete the annotations.
            cpt.undraw()
            redraw = False
        except AttributeError:
            pass

        self.components.remove(cpt)
        for node in cpt.nodes:
            self.nodes.remove(node, cpt)

        if redraw:
            self.ui.clear()
            self.redraw()

    def cpt_draw(self, cpt):

        cpt.draw(self, self.ui.layer)

        label_cpts = self.preferences.label_cpts

        if cpt.TYPE in ('A', 'O', 'W'):
            label_cpts = 'none'

        name = cpt.name
        value = cpt.value
        if value is None:
            value = ''

        if label_cpts == 'name+value':
            if name != value:
                label = name + '=' + value
            else:
                label = name
        elif label_cpts == 'value':
            if value != '':
                label = value
            else:
                label = name
        elif label_cpts == 'name':
            label = name
        elif label_cpts == 'none':
            label = ''
        else:
            raise RuntimeError('Unhandled label_cpts=' + label_cpts)

        if label != '':
            ann = Annotation(self.ui, *cpt.label_position, label)
            ann.draw(fontsize=18)
            cpt.annotations.append(ann)

        draw_nodes = self.preferences.draw_nodes
        if draw_nodes != 'none':
            for node in cpt.nodes:
                if node.port:
                    self.node_draw(node)
                    continue

                if draw_nodes == 'connections' and node.count < 3:
                    continue
                if draw_nodes == 'primary' and not node.is_primary:
                    continue
                self.node_draw(node)

        label_nodes = self.preferences.label_nodes
        if label_nodes != 'none':
            for node in cpt.nodes:

                if label_nodes == 'alpha' and not node.name[0].isalpha():
                    continue

                pos = array(node.position)
                pos[0] += 0.3
                pos[1] += 0.3
                ann = Annotation(self.ui, *pos, node.name)
                ann.draw(fontsize=18)
                cpt.annotations.append(ann)

    def cpt_make(self, cpt_key, cpt_kind=''):

        try:
            cpt_class_name = self.component_map[cpt_key][1]
        except KeyError:
            return None

        if cpt_class_name == '':
            return None

        cpt = cpt_make(cpt_class_name, cpt_kind)
        self.invalidate()
        return cpt

    def cpt_find(self, n1, n2):

        cpt2 = None
        for cpt in self.components:
            if (cpt.nodes[0].name == n1 and cpt.nodes[1].name == n2):
                cpt2 = cpt
                break
        if cpt2 is None:
            self.exception(
                'Cannot find a component with nodes %s and %s' % (n1, n2))
        return cpt2

    def cpt_place(self, cpt, x1, y1, x2, y2):
        """Place a component at the specified pair of positions.

        """

        positions = cpt.assign_positions(x1, y1, x2, y2)
        angle = degrees(atan2(y2 - y1, x2 - x1))
        cpt.angle = angle

        nodes = []
        for position in positions:
            node = self.nodes.make(*position, None, cpt)
            self.nodes.add(node)
            nodes.append(node)

        self.components.add_auto(cpt, *nodes)
        self.cpt_draw(cpt)

        self.select(cpt)
        self.dirty = True

        self.history.append((cpt, 'A'))

    def cut(self, cpt):

        self.delete(cpt)
        self.clipped = cpt

    def delete(self, cpt):

        self.cpt_delete(cpt)
        self.history.append((cpt, 'D'))

    def draw(self, cpt, **kwargs):

        if cpt is None:
            return
        cpt.draw(**kwargs)

    def export(self, filename):

        cct = self._cct
        cct.draw(filename)

    def invalidate(self):

        self._cct = None

    def load(self, filename):

        from lcapy import Circuit

        self.filename = filename

        self.components.clear()

        cct = Circuit(filename)

        self.load_from_circuit(cct)

    def load_from_circuit(self, cct):

        # TODO: use Lcapy parser

        sch = cct.sch

        try:
            # This will fail if have detached circuits unless nodes
            # are defined in the file.
            calculated = sch._positions_calculate()
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)
            return

        width, height = sch.width * self.STEP,  sch.height * self.STEP

        if calculated:
            # Centre the schematic.
            offsetx, offsety = self.snap((self.ui.XSIZE - width) / 2,
                                         (self.ui.YSIZE - height) / 2)
        else:
            offsetx, offsety = 0, 0

        vcs = []
        elements = cct.elements
        for elt in elements.values():

            # Handle schematic kind
            if 'kind' in elt.opts:
                kind = elt.opts['kind']
            else:
                kind = ''

            # Handle electrical kind
            if elt.keyword and elt.keyword[0] is not None:
                kind = elt.keyword[1]

            if elt.type == 'XX':
                # Ignore directives
                continue
            elif isinstance(elt, Eopamp):
                cpt = self.cpt_make('opamp')
            elif elt.type == 'A':
                cpt = self.annotation_make(elt, kind)
            else:
                cpt = self.cpt_make(elt.type.lower(), kind)
            if cpt is None:
                self.exception('Unhandled component ' + str(elt.name))
                return

            nodes = []
            for m, node1 in enumerate(elt.nodes[0:2]):

                try:
                    x1 = sch.nodes[node1.name].pos.x + offsetx
                    y1 = sch.nodes[node1.name].pos.y + offsety
                except KeyError:
                    # Handle opamp ground node
                    x1, y1 = 0, 0

                node = self.nodes.make(x1, y1, node1.name, cpt)
                self.nodes.add(node)
                nodes.append(node)
            if elt.type in ('R', 'NR'):
                cpt.value = elt.args[0]
            elif elt.type in ('C', 'L'):
                cpt.value = elt.args[0]
                cpt.initial_value = elt.args[1]
            elif elt.type in ('V', 'I', 'Z', 'Y'):
                cpt.value = elt.args[0]
            elif elt.type in ('E', 'G'):
                cpt.value = elt.args[0]
                if isinstance(elt, Eopamp):
                    for m, node1 in enumerate(elt.nodes[2:4]):
                        x1 = sch.nodes[node1.name].pos.x + offsetx
                        y1 = sch.nodes[node1.name].pos.y + offsety
                        node = self.nodes.make(x1, y1, node1.name, cpt)
                        self.nodes.add(node)
                        nodes.append(node)
                else:
                    vcs.append((cpt, elt.nodes[2].name, elt.nodes[3].name))

            elif elt.type in ('F', 'H'):
                cpt.value = elt.args[0]
                cpt.control = elt.args[1]

            elif elt.type in ('A', 'W', 'O', 'P', 'D'):
                pass
            else:
                self.exception('Unhandled component ' + elt)
                return

            attrs = []
            for opt, val in elt.opts.items():
                if opt in ('left', 'right', 'up', 'down', 'rotate', 'kind'):
                    continue

                def fmt(key, val):
                    if val == '':
                        return key
                    return '%s=%s' % (key, val)

                attrs.append(fmt(opt, val))
            cpt.attrs = ', '.join(attrs)
            cpt.opts = elt.opts

            self.components.add(cpt, elt.name, *nodes)
            self.cpt_draw(cpt)

        for cpt, n1, n2 in vcs:
            ccpt = self.cpt_find(n1, n2)
            if ccpt is not None:
                cpt.control = ccpt.name

    def move(self, xshift, yshift):
        # TODO
        pass

    def paste(self, x1, y1, x2, y2):

        if self.clipped is None:
            return
        cpt = copy(self.clipped)
        self.cpt_place(cpt, x1, y1, x2, y2)

    def rotate(self, angle):
        # TODO
        pass

    def save(self, filename):

        s = self.schematic()

        with open(filename, 'w') as fhandle:
            fhandle.write(s)
        self.dirty = False

    def schematic(self):

        s = '# Created by ' + self.ui.NAME + ' V' + self.ui.version + '\n'

        # Define node positions
        foo = [str(node) for node in self.nodes]
        s += '; nodes={' + ', '.join(foo) + '}' + '\n'

        try:
            s += self.components.as_sch(self.STEP)
        except Exception as e:
            self.exception(e)
            return

        # Note, need a newline so string treated as a netlist string
        s += '; ' + self.preferences.schematic_preferences() + '\n'
        return s

    def inspect_admittance(self, cpt):

        try:
            self.last_expr = self.cct[cpt.name].Y
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s admittance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_current(self, cpt):

        # TODO: FIXME for wire current
        try:
            self.last_expr = self.cct[cpt.name].i
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s current' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_impedance(self, cpt):

        try:
            self.last_expr = self.cct[cpt.name].Z
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s impe' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_norton_admittance(self, cpt):

        try:
            self.last_expr = self.cct[cpt.name].dpY
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s Norton admittance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_thevenin_impedance(self, cpt):

        try:
            self.last_expr = self.cct[cpt.name].dpZ
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s Thevenin impedance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_voltage(self, cpt):

        try:
            self.last_expr = self.cct[cpt.name].v
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s potential difference' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def show_node_voltage(self, node):

        try:
            self.last_expr = self.cct[node.name].v
            self.ui.show_expr_dialog(self.last_expr,
                                     'Node %s potential' % node.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def select(self, thing):

        self.selected = thing

    def snap(self, x, y):

        snap = self.SNAP
        x = (x + 0.5 * snap) // snap * snap
        y = (y + 0.5 * snap) // snap * snap
        return x, y

    def unselect(self):
        pass

    def view(self):

        cct = self._cct
        if cct is None:
            if self.ui.debug:
                import pdb
                pdb.set_trace()
            return
        cct.draw()

    def voltage_annotate(self, cpt):

        ann1 = Annotation(self.ui, *cpt.nodes[0].position, '+')
        ann2 = Annotation(self.ui, *cpt.nodes[1].position, '-')

        self.voltage_annotations.add(ann1)
        self.voltage_annotations.add(ann2)
        ann1.draw(color='red', fontsize=40)
        ann2.draw(color='blue', fontsize=40)

    @property
    def ground_node(self):

        return self.node_find('0')

    def node_draw(self, node):

        if node.port:
            self.ui.layer.stroke_circle(
                *node.position, self.preferences.node_size,
                color=self.preferences.node_color, alpha=1)
        else:
            self.ui.layer.stroke_filled_circle(
                *node.position, self.preferences.node_size,
                color=self.preferences.node_color, alpha=1)

    def node_find(self, nodename):

        for node in self.nodes:
            if node.name == nodename:
                return node
        return None

    def redo(self):

        # TODO
        pass

    def redraw(self):

        for cpt in self.components:
            self.cpt_draw(cpt)

    def undo(self):

        if self.history == []:
            return
        cpt, op = self.history.pop()
        if op == 'D':
            self.components.add(cpt, cpt.name, *cpt.nodes)
            self.cpt_draw(cpt)
            self.select(cpt)
        else:
            self.cpt_delete(cpt)
