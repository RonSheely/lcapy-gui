from ..annotation import Annotation
from ..annotations import Annotations
from .preferences import Preferences
from ..components.opamp import Opamp
from ..components.pos import Pos
from ..components.cpt_maker import cpt_make_from_cpt, cpt_make_from_type
from .history_event import HistoryEvent

from copy import copy
from math import atan2, degrees, sqrt
from numpy import nan, isnan
from lcapy import Circuit, expr
from lcapy.mnacpts import Cpt
from lcapy.nodes import parse_nodes
from lcapy.opts import Opts


class C:

    def __init__(self, accelerator, menu_name, cpt_type, kind):

        self.accelerator = accelerator
        self.menu_name = menu_name
        self.cpt_type = cpt_type
        self.kind = kind

    def __str__(self):

        return self.cpt_type


class UIModelBase:

    STEP = 2
    SNAP = 1
    SCALE = 0.25

    # Short-cut key, menu name, cpt type, kind
    component_map = {
        'y': C('y', 'Admittance', 'Y', ''),
        'c': C('c', 'Capacitor', 'C', ''),
        'cpe': C('', 'Constant phase element (CPE)', 'CPE', ''),
        'f': C('f', 'Current controlled current source', 'F', ''),
        'h': C('h', 'Current controlled voltage source', 'H', ''),
        'i': C('i', 'Current source', 'I', ''),
        'inamp': C('', 'Instrumention amplifier', 'inamp', ''),
        'd': C('d', 'Diode', 'D', ''),
        'fb': C('', 'Ferrite bead', 'FB', ''),
        'z': C('z', 'Impedance', 'Z', ''),
        'l': C('l', 'Inductor', 'L', ''),
        'opamp': C('', 'Opamp', 'opamp', ''),
        'fdopamp': C('', 'Fully differential opamp', 'fdopamp', ''),
        'o': C('o', 'Open circuit', 'O', ''),
        'p': C('p', 'Port', 'P', ''),
        'r': C('r', 'Resistor', 'R', ''),
        'nr': C('', 'Resistor (noiseless)', 'R', ''),
        'tf': C('tf', 'Transformer', 'TF', ''),
        'q': C('q', 'BJT', 'Q', ''),
        'j': C('j', 'JFET', 'J', ''),
        'm': C('m', 'MOSFET', 'M', ''),
        'v': C('v', 'Voltage source', 'V', ''),
        'g': C('g', 'Voltage controlled current source', 'G', ''),
        'e': C('e', 'Voltage controlled voltage source', 'E', ''),
        'w': C('w', 'Wire', 'W', ''),
    }

    # Short-cut key, menu name, cpt type, kind
    connection_map = {
        '0V': C('', '0V', 'W', '0V'),
        'ground': C('0', 'Ground', 'W', 'ground'),
        'sground': C('', 'Signal ground', 'W', 'sground'),
        'rground': C('', 'Rail ground', 'W', 'rground'),
        'cground': C('', 'Chassis ground', 'W', 'cground'),
        'vdd': C('', 'VDD', 'W', 'vdd'),
        'vss': C('', 'VSS', 'W', 'vss'),
        'vcc': C('', 'VCC', 'W', 'vcc'),
        'vee': C('', 'VEE', 'W', 'vee'),
        'input': C('', 'Input', 'W', 'input'),
        'output': C('', 'Output', 'W', 'output'),
        'bidir': C('', 'Bidirectional', 'W', 'bidir')
    }

    def __init__(self, ui):

        self.circuit = Circuit()
        self.ui = ui
        self._analysis_circuit = None
        self.pathname = ''
        self.voltage_annotations = Annotations()
        self.selected = None
        self.last_expr = None
        self.preferences = Preferences()
        self.dirty = False
        self.history = []
        self.clipboard = None
        self.select_pos = 0, 0
        self.dragged = False

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

            ground_node = list(self.circuit.nodes)[0]
            self.ui.show_info_dialog(
                'Defining node %s as the ground node.' % ground_node)

            # Add dummy ground node to first node
            net = 'W %s 0\n' % ground_node
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
        for node in self.circuit.nodes.values():
            if node.x < xmin:
                xmin = node.x
            if node.x > xmax:
                xmax = node.x
            if node.y < ymin:
                ymin = node.y
            if node.y > ymax:
                ymax = node.y
        return xmin, ymin, xmax, ymax

    def choose_cpt_name(self, cpt_type):

        if cpt_type in ('opamp', 'fdopamp', 'inamp'):
            cpt_type = 'E'

        num = 1
        while True:
            name = cpt_type + str(num)
            if name not in self.circuit.elements:
                return name
            num += 1

    def con_create(self, thing, x1, y1, x2, y2):
        """Create a new connection."""

        cpt_type = thing.cpt_type
        if cpt_type == '':
            return None

        return self.thing_create(cpt_type, x1, y1, x2, y2, kind='-' + thing.kind)

    def copy(self, cpt):

        self.clipboard = cpt

    @property
    def cpt_selected(self):

        return isinstance(self.selected, Cpt)

    def cpt_create(self, cpt_type, x1, y1, x2, y2):
        """Create a new component."""

        s = sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if s < 0.2:
            self.exception('Nodes too close to create component')
            return None

        return self.thing_create(cpt_type, x1, y1, x2, y2)

    def cpt_delete(self, cpt):

        if self.ui.debug:
            print('Deleting %s' % cpt)

        self.select(None)

        redraw = True
        try:
            cpt.undraw()
            redraw = False
        except AttributeError:
            pass

        self.circuit.remove(cpt.name)
        self.invalidate()

        if redraw:
            self.ui.clear()
            self.redraw()

    def cpt_draw(self, cpt, **kwargs):

        gcpt = cpt.gcpt
        if gcpt is None:
            return

        gcpt.draw(self, **kwargs)

        label_cpts = self.preferences.label_cpts

        if gcpt.type in ('A', 'O', 'W', 'X'):
            label_cpts = 'none'

        name = cpt.name

        try:
            if cpt.type in ('F', 'H'):
                value = cpt.args[1]
            elif cpt.type in ('P', ):
                value = None
            else:
                value = cpt.args[0]
        except IndexError:
            value = None

        if value is None:
            value = ''
            value_latex = ''
        else:
            value_latex = '$' + expr(value).latex() + '$'

        label = ''
        if label_cpts == 'name+value':
            if name != value and gcpt.has_value:
                label = name + '=' + value_latex
            else:
                label = name
        elif label_cpts == 'value':
            if value != '':
                label = value_latex
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
            for node in gcpt.drawn_nodes:
                if node.port:
                    self.node_draw(node)
                    continue

                if draw_nodes == 'connections' and node.count < 3:
                    continue
                if draw_nodes == 'primary' and not node.primary:
                    continue
                self.node_draw(node)

        label_nodes = self.preferences.label_nodes
        if label_nodes != 'none':
            for node in gcpt.labelled_nodes:
                if node.name[0] == '_':
                    continue

                if label_nodes == 'alpha' and not node.name[0].isalpha():
                    continue

                x, y = node.pos.x, node.pos.y
                # Should be x -= 0.1 but need to right justify.
                x += 0.1
                y += 0.1
                ann = Annotation(self.ui, x, y, node.name)
                ann.draw(fontsize=18)
                gcpt.annotations.append(ann)

    def cpt_find(self, node_name1, node_name2):

        fcpt = None
        for cpt in self.circuit:
            if (cpt.nodes[0].name == node_name1 and cpt.nodes[1].name == node_name2):
                fcpt = cpt
                break
        if fcpt is None:
            self.exception(
                'Cannot find a component with nodes %s and %s' % (node_name1, node_name2))
        return fcpt

    def cpt_move(self, cpt, xshift, yshift, move_nodes=False):

        isolated = True
        for node in cpt.nodes:
            if node.count > 1:
                isolated = False
                break

        if isolated or move_nodes:

            for node in cpt.nodes:
                # TODO: handle snap
                node.pos.x += xshift
                node.pos.y += yshift

            # TODO: only redraw cpts that have moved
            gcpt = cpt.gcpt
            gcpt.undraw()
            gcpt.draw(self)
        else:
            # Alternatively, assign new nodes for the cpt being moved
            # if the nodes are shared.

            gcpt = cpt.gcpt
            x1 = gcpt.node1.x + xshift
            y1 = gcpt.node1.y + yshift
            x2 = gcpt.node2.x + xshift
            y2 = gcpt.node2.y + yshift

            self.cpt_modify_nodes(cpt, x1, y1, x2, y2)

    def cpt_modify_nodes(self, cpt, x1, y1, x2, y2):

        gcpt = cpt.gcpt
        cpt_key = gcpt.type

        self.cpt_delete(gcpt)
        newcpt = self.cpt_create(cpt_key, x1, y1, x2, y2)

        # TODO: tidy
        newgcpt = newcpt.gcpt
        newgcpt.kind = gcpt.kind
        newcpt.args = cpt.args
        newcpt.opts.clear()
        newcpt.opts.add(gcpt.attr_string(newgcpt.node1.x, newgcpt.node1.y,
                                         newgcpt.node2.x, newgcpt.node2.y,
                                         self.STEP))

    def cpt_remake(self, cpt):

        gcpt = cpt.gcpt

        if cpt.is_dependent_source and gcpt.type not in ('Eopamp',
                                                         'Efdopamp', 'Einamp'):
            try:
                newcpt = cpt._change_control(gcpt.control)
            except Exception:
                self.exception('Control component %s for %s deleted' %
                               (gcpt.control, cpt.name))
                return
        elif gcpt.cpt_kind == cpt._kind:
            newcpt = cpt
        elif gcpt.type not in ('Eopamp', 'Efdopamp', 'Einamp'):
            try:
                newcpt = cpt._change_kind(gcpt.cpt_kind)
            except Exception:
                self.exception('Cannot change kind for %s' % cpt.name)
                return
        else:
            newcpt = cpt

        if gcpt.name != cpt.name:
            try:
                newcpt = newcpt._change_name(gcpt.name)
            except Exception:
                self.exception('Cannot change name for %s' % cpt.name)
                return

        if gcpt.mirror ^ ('mirror' in newcpt.opts):
            # TODO, add mirror method...
            if gcpt.type == 'Eopamp':
                newcpt.nodes[2], newcpt.nodes[3] = newcpt.nodes[3], newcpt.nodes[2]
            elif gcpt.type == 'Efdopamp':
                newcpt.nodes[2], newcpt.nodes[3] = newcpt.nodes[3], newcpt.nodes[2]
            elif gcpt.type == 'Einamp':
                newcpt.nodes[2], newcpt.nodes[3] = newcpt.nodes[3], newcpt.nodes[2]
            elif gcpt.type in ('J', 'M', 'Q'):
                newcpt.nodes[2], newcpt.nodes[0] = newcpt.nodes[0], newcpt.nodes[2]
            else:
                print('Trying to change mirror for ' + str(newcpt))

        newcpt.opts.clear()
        newcpt.opts.add(gcpt.attr_string(gcpt.node1.x, gcpt.node1.y,
                                         gcpt.node2.x, gcpt.node2.y, self.STEP))

        newcpt.gcpt = gcpt

    def cut(self, cpt):

        self.delete(cpt)
        self.clipboard = cpt

    def delete(self, cpt):

        self.cpt_delete(cpt)
        self.history.append(HistoryEvent('D', cpt))

    def draw(self, cpt, **kwargs):

        if cpt is None:
            return
        cpt.draw(**kwargs)

    def export(self, pathname):

        cct = Circuit(self.schematic())
        cct.draw(pathname)

    def invalidate(self):

        self._analysis_circuit = None

    def load(self, pathname):

        from lcapy import Circuit

        self.pathname = pathname

        with open(pathname) as f:
            line = f.readline()
            if line.startswith(r'\begin{tikz'):
                self.ui.show_error_dialog('Cannot load Circuitikz macro file')
                return

        try:
            circuit = Circuit(pathname)
        except Exception as e:
            self.exception(e)
            return

        return self.load_from_circuit(circuit)

    def load_from_circuit(self, circuit):

        self.circuit = circuit
        positions = None
        for cpt in self.circuit.elements.values():
            if cpt.type == 'XX' and 'nodes' in cpt.opts:
                positions = parse_nodes(cpt.opts['nodes'])
                break

        if positions is not None:
            for k, v in self.circuit.nodes.items():
                try:
                    v.pos = positions[k]
                except KeyError:
                    v.pos = None

        else:

            # Node positions not defined.

            sch = self.circuit.sch

            try:
                # This will fail if have detached components.
                calculated = sch._positions_calculate()
            except (AttributeError, ValueError, RuntimeError) as e:
                self.exception(e)
                return

            width, height = sch.width * self.STEP, sch.height * self.STEP

            # Centre the schematic.
            xsize = self.ui.canvas.drawing.xsize
            ysize = self.ui.canvas.drawing.ysize
            offsetx, offsety = self.snap_to_grid((xsize - width) / 2,
                                                 (ysize - height) / 2)
            for node in sch.nodes.values():
                node.pos.x += offsetx
                node.pos.y += offsety
                # May have split nodes...
                if node.name in circuit.nodes:
                    circuit.nodes[node.name].pos = node.pos

        self.remove_directives()

        for cpt in self.circuit.elements.values():
            if cpt.type == 'XX':
                cpt.gcpt = None
                continue
            try:
                gcpt = cpt_make_from_cpt(cpt)
            except Exception as e:
                gcpt = None
                self.exception(e)

            cpt.gcpt = gcpt

        self.invalidate()
        self.redraw()

    def paste(self, x1, y1, x2, y2):

        if self.clipboard is None:
            return

        return self.thing_create(self.clipboard.type, x1, y1, x2, y2)

    def possible_control_names(self):

        cpts = self.circuit.elements.values()
        names = [c.name for c in cpts if c.name[0] != 'W']
        return names

    def remove_directives(self):

        elt_list = list(self.circuit.elements.values())
        if elt_list == []:
            return

        cpt = elt_list[-1]
        if cpt.type == 'XX':
            # TODO: make more robust
            # This tries to remove the schematic attributes.
            # Perhaps parse this and set preferences but this
            # might be confusing.
            self.circuit.remove(cpt.name)
            cpt = elt_list[0]

        if cpt.type == 'XX' and cpt._string.startswith('# Created by lcapy'):
            self.circuit.remove(cpt.name)

        if len(elt_list) > 1:
            cpt = elt_list[1]
            if cpt.type == 'XX' and cpt._string.startswith('; nodes='):
                self.circuit.remove(cpt.name)

    def rotate(self, angle):
        # TODO
        pass

    def save(self, pathname):

        s = self.schematic()

        with open(pathname, 'w') as fhandle:
            fhandle.write(s)
        self.dirty = False

    def schematic(self):

        s = '# Created by ' + self.ui.NAME + ' V' + self.ui.version + '\n'

        # Define node positions
        foo = [str(node) for node in self.circuit.nodes.values()
               if node.pos is not None and not isnan(node.pos.x)]

        s += '; nodes={' + ', '.join(foo) + '}' + '\n'

        for cpt in self.circuit.elements.values():
            s += str(cpt) + '\n'

        # FIXME, remove other preference string
        # Note, need a newline so string treated as a netlist string
        s += '; ' + self.preferences.schematic_preferences() + '\n'
        return s

    def thing_create(self, cpt_type, x1, y1, x2, y2, kind=''):

        from lcapy.mnacpts import Cpt

        cpt_name = self.choose_cpt_name(cpt_type)
        gcpt = cpt_make_from_type(cpt_type, cpt_name, kind=kind)
        if gcpt is None:
            return None

        all_node_names = list(self.circuit.nodes)
        node_names = []
        positions = gcpt.assign_positions(x1, y1, x2, y2)

        for m, position in enumerate(positions):
            if position is None:
                continue

            node = self.circuit.nodes.by_position(position)
            if node is None:
                node_name = gcpt.choose_node_name(m, all_node_names)
                all_node_names.append(node_name)
            else:
                node_name = node.name
            node_names.append(node_name)

        netitem = gcpt.netitem(node_names, x1, y1, x2, y2, self.STEP)

        if self.ui.debug:
            print('Adding ' + netitem)

        cpt = self.circuit.add(netitem)
        self.invalidate()

        if not isinstance(cpt, Cpt):
            # Support older versions of Lcapy
            cpt = self.circuit[cpt_name]

        for m, position in enumerate(positions):
            cpt.nodes[m].pos = Pos(position)

        attr_string = netitem.split(';', 1)[1]
        gcpt.update(nodes=cpt.nodes, opts=Opts(attr_string))

        # Duck type
        cpt.gcpt = gcpt

        self.cpt_draw(cpt)

        self.history.append(HistoryEvent('A', cpt))

        self.select(cpt)

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

    def inspect_noise_current(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].V.n
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s noise current' % cpt.name)
        except (AttributeError, ValueError, RuntimeError) as e:
            self.exception(e)

    def inspect_noise_voltage(self, cpt):

        try:
            self.last_expr = self.analysis_circuit[cpt.name].V.n
            self.ui.show_expr_dialog(self.last_expr,
                                     '%s noise voltage' % cpt.name)
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

    def is_close_to(self, x, xc):

        return abs(x - xc) < 0.3

    def is_on_grid_x(self, x):

        xs = self.snap_to_grid_x(x)
        return x == xs

    def is_on_grid_y(self, y):

        ys = self.snap_to_grid_y(y)
        return y == ys

    def is_on_grid(self, x, y):

        return self.is_on_grid_x(x) and self.is_on_grid_y(y)

    def snap(self, x, y):

        # Snap to closest known node then snap to grid.
        node = self.closest_node(x, y)
        if node is not None:
            return node.x, node.y

        if self.preferences.snap_grid == 'true':

            if len(self.cursors) > 0:
                xc = self.cursors[0].x
                yc = self.cursors[0].y
                if self.is_close_to(x, xc):
                    x = xc
                else:
                    x = self.snap_to_grid_x(x)
                if self.is_close_to(y, yc):
                    y = yc
                else:
                    y = self.snap_to_grid_y(y)
            else:
                x, y = self.snap_to_grid(x, y)

        return x, y

    def snap_to_grid_x(self, x):

        snap = self.SNAP
        x = (x + 0.5 * snap) // snap * snap
        return x

    def snap_to_grid_y(self, y):

        snap = self.SNAP
        y = (y + 0.5 * snap) // snap * snap
        return y

    def snap_to_grid(self, x, y):

        return self.snap_to_grid_x(x), self.snap_to_grid_y(y)

    def unselect(self):
        pass

    def view(self):

        cct = Circuit(self.schematic())
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

        if node.pos is None:
            print('Pos unknown for ' + str(node))
            return

        if node.port:
            self.ui.sketcher.stroke_circle(
                node.x, node.y, self.preferences.node_size,
                color=self.preferences.node_color, alpha=1)
        else:
            self.ui.sketcher.stroke_filled_circle(
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
            if cpt == self.selected:
                self.cpt_draw(cpt, color='red')
            else:
                self.cpt_draw(cpt)

        # Should redraw nodes on top to blank out wires on top of ports

    def undo(self):

        if self.history == []:
            return
        event = self.history.pop()
        cpt = event.cpt

        if self.ui.debug:
            print('Undo ' + event.code)

        if event.code == 'D':
            self.circuit.add(str(cpt))

            # Copy node positions
            new_cpt = self.circuit.elements[cpt.name]
            for m, node in enumerate(cpt.nodes):
                new_cpt.nodes[m].pos = node.pos
            new_cpt.gcpt = cpt.gcpt

            self.cpt_draw(cpt)
            self.select(cpt)

        elif event.code == 'M':
            for node, pos in zip(cpt.nodes, event.nodes):
                node.pos.x = pos[0]
                node.pos.y = pos[1]

            self.select(cpt)
            self.on_redraw()

        elif event.code == 'A':
            self.cpt_delete(cpt)

        else:
            raise RuntimeError('Unknown event code ' + event.code)

        self.invalidate()
