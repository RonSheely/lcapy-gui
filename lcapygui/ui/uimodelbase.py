from ..annotation import Annotation
from ..annotations import Annotations
from .preferences import Preferences
from ..components.cpt_maker import cpt_make
from copy import copy
from numpy import array
from math import atan2, degrees, sqrt
from lcapy import Circuit
from lcapy.mnacpts import Cpt, Eopamp
from lcapy.nodes import parse_nodes


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

        self.circuit = Circuit()
        self.ui = ui
        self._analysis_circuit = None
        self.filename = ''
        self.voltage_annotations = Annotations()
        self.selected = None
        self.last_expr = None
        self.preferences = Preferences()
        self.dirty = False
        self.history = []
        self.clipboard = None

    @property
    def analysis_circuit(self):
        """This like circuit but it has an added ground node if one does
        not exist.

        """

        if self._analysis_circuit is not None:
            return self._analysis_circuit

        if self.circuit.elements == {}:
            self.exception('No circuit defined')
            return None

        self._analysis_circuit = self.circuit.copy()

        if self.ground_node is None:
            # Add dummy ground node to first node
            net = 'W %s 0\n' % list(self.circuit.nodes)[0]
            self.analysis_circuit.add(net)

        try:
            self._analysis_circuit[0]
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)
            return None

        return self._analysis_circuit

    def bounding_box(self):

        if len(self.circuit.nodes) == 0:
            return None

        xmin = 1000
        xmax = 0
        ymin = 1000
        ymax = 0
        for node in self.circuit.nodes:
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
        """Create a new connection."""

        try:
            cpt_type = self.connection_map[con_key][1]
        except KeyError:
            return None

        if cpt_type == '':
            return None

        return self.thing_create(cpt_type, x1, y1, x2, y2)

    def choose_cpt_name(self, cpt_type):

        num = 1
        while True:
            name = cpt_type + str(num)
            if name not in self.circuit.elements:
                return name
            num += 1

    def choose_node_name(self, nodes):

        num = 1
        while True:
            name = str(num)
            if name not in nodes:
                return name
            num += 1

    def con_make(self, con_key, kind='', style=''):

        try:
            cpt_type = self.connection_map[con_key][1]
            if kind == '':
                kind = self.connection_map[con_key][2]
        except KeyError:
            return None

        if cpt_type == '':
            return None

        gcpt = cpt_make(cpt_type, kind, style)
        self.invalidate()
        return gcpt

    def copy(self, cpt):

        self.clipboard = cpt

    @property
    def cpt_selected(self):

        return isinstance(self.selected, Cpt)

    def cpt_create(self, cpt_key, x1, y1, x2, y2):
        """Create a new component."""

        s = sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if s < 0.2:
            self.exception('Nodes too close to create component')
            return

        try:
            cpt_type = self.component_map[cpt_key][1]
        except KeyError:
            return None

        if cpt_type == '':
            return None

        return self.thing_create(cpt_type, x1, y1, x2, y2)

    def cpt_delete(self, cpt):

        self.select(None)

        redraw = True
        try:
            # This should also delete the annotations.
            cpt.undraw()
            redraw = False
        except AttributeError:
            pass

        self.circuit.remove(cpt.name)

        if redraw:
            self.ui.clear()
            self.redraw()

    def cpt_draw(self, cpt):

        gcpt = cpt.gcpt
        if gcpt is None:
            return

        gcpt.draw(self, self.ui.layer)

        label_cpts = self.preferences.label_cpts

        if gcpt.type in ('A', 'O', 'W'):
            label_cpts = 'none'

        name = cpt.name

        # FIXME
        value = gcpt.value

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
            ann = Annotation(self.ui, gcpt.label_position.x,
                             gcpt.label_position.y, label)
            ann.draw(fontsize=18)
            gcpt.annotations.append(ann)

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

                pos = array(node.pos)
                pos[0] += 0.3
                pos[1] += 0.3
                ann = Annotation(self.ui, *pos, node.name)
                ann.draw(fontsize=18)
                gcpt.annotations.append(ann)

    def cpt_find(self, n1, n2):

        cpt2 = None
        for cpt in self.circuit:
            if (cpt.nodes[0].name == n1 and cpt.nodes[1].name == n2):
                cpt2 = cpt
                break
        if cpt2 is None:
            self.exception(
                'Cannot find a component with nodes %s and %s' % (n1, n2))
        return cpt2

    def cut(self, cpt):

        self.delete(cpt)
        self.clipboard = cpt

    def delete(self, cpt):

        self.cpt_delete(cpt)
        self.history.append((cpt, 'D'))

    def draw(self, cpt, **kwargs):

        if cpt is None:
            return
        cpt.draw(**kwargs)

    def export(self, filename):

        cct = self.circuit
        cct.draw(filename)

    def invalidate(self):

        self._analysis_circuit = None

    def load(self, filename):

        from lcapy import Circuit

        self.filename = filename

        with open(filename) as f:
            line = f.readline()
            if line.startswith(r'\begin{tikz'):
                self.ui.show_error_dialog('Cannot load Circuitikz macro file')
                return

        try:
            self.circuit = Circuit(filename)
        except Exception as e:
            self.exception(e)
            return

        positions = None
        for cpt in self.circuit.elements.values():
            if cpt.type == 'XX' and 'nodes' in cpt.opts:
                positions = parse_nodes(cpt.opts['nodes'])

        if positions is None:
            self.exception('Node positions not defined')
            return

        for k, v in self.circuit.nodes.items():
            v.pos = positions[k]

        for cpt in self.circuit.elements.values():
            if cpt.type == 'XX':
                cpt.gcpt = None
                continue
            try:
                gcpt = cpt_make(cpt.type)
                gcpt.nodes = cpt.nodes
            except Exception as e:
                cgpt = None
                self.exception(e)

            cpt.gcpt = gcpt

        self.redraw()

    def move(self, xshift, yshift):
        # TODO
        pass

    def paste(self, x1, y1, x2, y2):

        if self.clipboard is None:
            return

        return self.thing_create(self.clipboard.type, x1, y1, x2, y2)

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
        foo = [str(node) for node in self.circuit.nodes.values()]
        s += '; nodes={' + ', '.join(foo) + '}' + '\n'

        s += str(self.circuit) + '\n'

        # Note, need a newline so string treated as a netlist string
        s += '; ' + self.preferences.schematic_preferences() + '\n'
        return s

    def thing_create(self, cpt_type, x1, y1, x2, y2):

        gcpt = cpt_make(cpt_type)

        positions = gcpt.assign_positions(x1, y1, x2, y2)

        cpt_name = self.choose_cpt_name(gcpt.type)
        net_parts = [cpt_name]

        nodes = list(self.circuit.nodes)

        for m, position in enumerate(positions):
            node = self.circuit.nodes.by_position(position)
            if node is None:
                node_name = self.choose_node_name(nodes)
                nodes.append(node_name)
            else:
                node_name = node.name
            net_parts.append(node_name)

        net = ' '.join(net_parts)

        if self.ui.debug:
            print('Adding ' + net)

        cct = self.circuit.add(net)
        cpt = cct[cpt_name]

        for m, position in enumerate(positions):
            cpt.nodes[m].pos = position

        # Duck type
        cpt.gcpt = gcpt
        gcpt.nodes = cpt.nodes

        self.cpt_draw(cpt)

        self.history.append((cpt, 'A'))

        return cpt

    def inspect_admittance(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].Y
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s admittance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_current(self, cpt):

        # TODO: FIXME for wire current
        try:
            self.last_expr = self.analysis_circuit[cpt.name].i
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s current' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_impedance(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].Z
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s impe' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_norton_admittance(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].dpY
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s Norton admittance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_thevenin_impedance(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].dpZ
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s Thevenin impedance' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_voltage(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].v
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s potential difference' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def show_node_voltage(self, node):

        try:
            self.last_expr = self.analysis_circuit[node.name].v
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

        cct = self.circuit
        cct.draw()

    def voltage_annotate(self, cpt):

        ann1 = Annotation(self.ui, *cpt.nodes[0].pos, '+')
        ann2 = Annotation(self.ui, *cpt.nodes[1].pos, '-')

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
                node.x, node.y, self.preferences.node_size,
                color=self.preferences.node_color, alpha=1)
        else:
            self.ui.layer.stroke_filled_circle(
                node.x, node.y, self.preferences.node_size,
                color=self.preferences.node_color, alpha=1)

    def node_find(self, nodename):

        for node in self.circuit.nodes.values():
            if node.name == nodename:
                return node
        return None

    def redo(self):

        # TODO
        pass

    def redraw(self):

        for cpt in self.circuit.elements.values():
            self.cpt_draw(cpt)

    def undo(self):

        if self.history == []:
            return
        cpt, op = self.history.pop()
        if op == 'D':
            self.circuit.add(str(cpt))

            # Copy node positions
            new_cpt = self.circuit.elements[cpt.name]
            for m, node in enumerate(cpt.nodes):
                new_cpt.nodes[m].pos = node.pos
            new_cpt.gcpt = cpt.gcpt

            self.cpt_draw(cpt)
            self.select(cpt)
        else:
            self.cpt_delete(cpt)
        self.invalidate()
