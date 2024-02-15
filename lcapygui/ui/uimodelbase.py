from ..annotation import Annotation
from ..annotations import Annotations
from .preferences import Preferences
from ..components.opamp import Opamp
from ..components.pos import Pos
from ..components.cpt_maker import gcpt_make_from_cpt, gcpt_make_from_type
from .history import History
from .history_event import HistoryEvent
from warnings import warn

from copy import copy
from math import atan2, degrees, sqrt, cos, sin
from numpy import nan, isnan, floor, array, dot, sqrt
from lcapy import Circuit, expr
from lcapy.mnacpts import Cpt
from lcapy.node import Node
from lcapy.nodes import parse_nodes
from lcapy.opts import Opts


class Thing:
    """
    Thing Class

    Explanation
    ===========
    Stores all relevant information for creating a new component 'thing'

    Attributes
    ==========
    accelerator : str
    menu_name : str
    cpt_type : str
    kind : str
    """

    def __init__(self, accelerator, menu_name, cpt_type, kind):

        self.accelerator = accelerator
        self.menu_name = menu_name
        self.cpt_type = cpt_type
        self.kind = kind

    def __str__(self):

        return self.cpt_type


class UIModelBase:

    SCALE = 0.25

    # Short-cut key, menu name, cpt type, kind
    component_map = {
        'y': Thing('y', 'Admittance', 'Y', ''),
        'c': Thing('c', 'Capacitor', 'C', ''),
        'cpe': Thing('', 'Constant phase element (CPE)', 'CPE', ''),
        'f': Thing('f', 'Current controlled current source', 'F', ''),
        'h': Thing('h', 'Current controlled voltage source', 'H', ''),
        'i': Thing('i', 'Current source', 'I', ''),
        'inamp': Thing('', 'Instrumention amplifier', 'inamp', ''),
        'd': Thing('d', 'Diode', 'D', ''),
        'fb': Thing('', 'Ferrite bead', 'FB', ''),
        'z': Thing('z', 'Impedance', 'Z', ''),
        'l': Thing('l', 'Inductor', 'L', ''),
        'opamp': Thing('', 'Opamp', 'opamp', ''),
        'fdopamp': Thing('', 'Fully differential opamp', 'fdopamp', ''),
        'o': Thing('o', 'Open circuit', 'O', ''),
        'p': Thing('p', 'Port', 'P', ''),
        'r': Thing('r', 'Resistor', 'R', ''),
        'nr': Thing('', 'Resistor (noiseless)', 'R', ''),
        'switch': Thing('', 'Switch', 'SW', ''),
        'tf': Thing('tf', 'Transformer', 'TF', ''),
        'q': Thing('q', 'BJT', 'Q', ''),
        'j': Thing('j', 'JFET', 'J', ''),
        'm': Thing('m', 'MOSFET', 'M', ''),
        'v': Thing('v', 'Voltage source', 'V', ''),
        'g': Thing('g', 'Voltage controlled current source', 'G', ''),
        'e': Thing('e', 'Voltage controlled voltage source', 'E', ''),
        'w': Thing('w', 'Wire', 'W', ''),
        'dw': Thing('', 'Dynamic Wire', 'DW', ''),
    }

    # Short-cut key, menu name, cpt type, kind
    connection_map = {
        '0V': Thing('', '0V', 'W', '-0V'),
        'ground': Thing('0', 'Ground', 'W', '-ground'),
        'sground': Thing('', 'Signal ground', 'W', '-sground'),
        'rground': Thing('', 'Rail ground', 'W', '-rground'),
        'cground': Thing('', 'Chassis ground', 'W', '-cground'),
        'vdd': Thing('', 'VDD', 'W', '-vdd'),
        'vss': Thing('', 'VSS', 'W', '-vss'),
        'vcc': Thing('', 'VCC', 'W', '-vcc'),
        'vee': Thing('', 'VEE', 'W', '-vee'),
        'input': Thing('', 'Input', 'W', '-input'),
        'output': Thing('', 'Output', 'W', '-output'),
        'bidir': Thing('', 'Bidirectional', 'W', '-bidir')
    }


    def __init__(self, ui):
        """
        Initialise the UI model
        :param ui.tk.lcapytk.LcapyTk ui: tkinter UI interface
        """
        self.circuit = Circuit()
        self.ui = ui
        self._analysis_circuit = None
        self.pathname = ''
        self.voltage_annotations = Annotations()
        self.selected = None
        self.last_expr = None
        self.preferences = Preferences()
        self.first_use = not self.preferences.load()
        self.preferences.apply()
        self.dirty = False
        self.history = History()
        self.recall = History()
        self.clipboard = None
        self.select_pos = 0, 0
        self.mouse_position = (0, 0)
        self.dragged = False
        self.zoom_factor = 1

    @property
    def node_spacing(self):

        return self.preferences.node_spacing

    @property
    def grid_spacing(self):

        return self.preferences.grid_spacing

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

    def apply(self, event, inverse):
        cpt = event.cpt
        code = event.code
        # Code:
        # A = add
        # D = delete
        # M = move
        # J = join (nodes)
        # S = split (nodes)

        if inverse:
            code = {'A': 'D', 'D': 'A', 'M': 'M', 'J': 'S', 'S': 'J'}[code]

        if code == 'A':
            newcpt = self.circuit.add(str(cpt))

            # Copy node positions
            new_cpt = self.circuit.elements[cpt.name]
            for m, node in enumerate(cpt.nodes):
                new_cpt.nodes[m].pos = node.pos
            new_cpt.gcpt = cpt.gcpt
            new_cpt.gcpt.nodes = cpt.gcpt.nodes

            self.cpt_draw(new_cpt)
            self.select(new_cpt)

        elif code == 'D':
            self.cpt_delete(cpt)

        elif code == 'M':
            # Check if moving a component or a node
            if isinstance(cpt, Cpt):
                nodes = event.from_nodes if inverse else event.to_nodes

                for node, pos in zip(cpt.nodes, nodes):
                    node.pos.x = pos[0]
                    node.pos.y = pos[1]

                self.select(cpt)
            else:
                node = cpt
                pos = event.from_nodes[0] if inverse else event.to_nodes[0]

                node.pos.x = pos[0]
                node.pos.y = pos[1]

                # If a subsequent join occurred, redo that too
                if self.recall[-1].code == 'J':
                    self.redo()

                self.select(node)
            self.on_redraw()
        elif code == 'J':
            self.node_join(event.from_nodes)
        elif code == 'S':
            connected_from = cpt
            new_node = event.from_nodes
            existing_node = event.to_nodes
            # split the nodes
            self.node_split(existing_node, new_node, connected_from)

            # If a preceding movement occurred, undo that too
            if self.history[-1].code == 'M':
                self.undo()

        # The network has changed
        self.invalidate()

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

    def copy(self, cpt):

        self.clipboard = cpt

    @property
    def cpt_selected(self):

        return isinstance(self.selected, Cpt)

    @property
    def node_selected(self):

        return isinstance(self.selected, Node)

    def cpt_create(self, cpt_type, x1, y1, x2, y2, kind=None):
        """
        TODO: Check
        Create a new component
        :param cpt_type: The component to create ('r' = resistor, etc.)
        :param x1: x position of the first node
        :param y1: y position of the first node
        :param x2: x position of the second node
        :param y2: y position of the second node
        :return: The instance of the component
        """

        s = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if s < 0.2:
            self.exception('Nodes too close to create component')
            return None

        cpt = self.thing_create(cpt_type, x1, y1, x2, y2, kind)
        self.history.append(HistoryEvent('A', cpt))
        self.select(cpt)
        return cpt

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

        try:
            gcpt = cpt.gcpt
        except AttributeError:
            breakpoint()

        if gcpt is None:
            return

        if "color" not in kwargs:
            kwargs["color"] = self.preferences.color('line')

        gcpt.draw(self, **kwargs)

        label_style = self.preferences.label_style

        if gcpt.type in ('A', 'O', 'W'):
            label_style = 'none'

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
        alabel = ''
        if label_style == 'name=value':
            if name != value and gcpt.has_value:
                label = name + '=' + value_latex
            else:
                label = name
        elif label_style == 'stacked':
            if name != value and gcpt.has_value:
                label = name + '\n' + value_latex
            else:
                label = name
        elif label_style == 'split':
            label = name
            if name != value and gcpt.has_value:
                alabel = value_latex
        elif label_style == 'value':
            if value != '':
                label = value_latex
        elif label_style == 'name':
            label = name
        elif label_style == 'none':
            label = ''
        else:
            raise RuntimeError('Unhandled label_style=' + label_style)

        # Perhaps use {} to force no label?
        if gcpt.label != '':
            label = gcpt.label
            alabel = None

        if gcpt.alabel != '':
            alabel = gcpt.alabel

        if label != '':
            ann = Annotation.make_label(self.ui, gcpt.midpoint,
                                        gcpt.angle, float(gcpt.scale),
                                        gcpt.label_offset_pos,
                                        gcpt.label_alignment, label)
            ann.draw(fontsize=self.preferences.font_size *
                     self.zoom_factor * self.preferences.line_width_scale)
            gcpt.annotations.append(ann)

        if alabel != '' and gcpt.annotation_offset_pos:
            ann = Annotation.make_label(self.ui, gcpt.midpoint,
                                        gcpt.angle, float(gcpt.scale),
                                        gcpt.annotation_offset_pos,
                                        gcpt.annotation_alignment,
                                        alabel)
            ann.draw(fontsize=self.preferences.font_size *
                     self.zoom_factor * self.preferences.line_width_scale)
            gcpt.annotations.append(ann)

        draw_nodes = self.preferences.draw_nodes
        if draw_nodes != 'none':
            dnodes = []
            for node in gcpt.drawn_nodes:
                # Ignore implict nodes
                if node.is_implicit:
                    continue

                if node.port:
                    dnodes.append(node)
                    continue

                if draw_nodes == 'connections' and node.count < 3:
                    continue
                if draw_nodes == 'primary' and not node.primary:
                    continue
                dnodes.append(node)

            for node in dnodes:
                self.node_draw(node)

        label_nodes = self.preferences.label_nodes
        if label_nodes != 'none':
            for node in gcpt.labelled_nodes:

                # Don't label a node that is not drawn
                if not node.is_drawn:
                    continue

                if node.name[0] == '_':
                    continue

                if label_nodes == 'alpha' and not node.name[0].isalpha():
                    continue

                x, y = node.pos.x, node.pos.y
                # Should be x -= 0.1 but need to right justify.
                x += 0.1
                y += 0.1
                ann = Annotation(self.ui, x, y, node.name)
                ann.draw(fontsize=self.preferences.font_size *
                         self.zoom_factor * self.preferences.line_width_scale)
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
            # If the component is not connected to another component,
            # or if we wish to move all the components sharing the
            # a node with the selected component, we can just move the nodes
            for node in cpt.nodes:
                self.node_move(node, node.pos.x + xshift, node.pos.y + yshift)

        else:
            # Alternatively, we need to detach the component and
            # assign new nodes if the nodes are shared.

            gcpt = cpt.gcpt
            x1 = gcpt.node1.x + xshift
            y1 = gcpt.node1.y + yshift
            x2 = gcpt.node2.x + xshift
            y2 = gcpt.node2.y + yshift

            self.cpt_modify_nodes(cpt, x1, y1, x2, y2)

    def node_move(self, node, new_x, new_y):
        """
        Changes the x, y position of a given node to the new_x, new_y position
        Then, redraws all connected components

        Parameters
        ==========
        node : lcapy.nodes.Node
            The node to move
        new_x : float
            The new x coordinate
        new_y : float
            The new y coordinate
        """

        # New position of nodes
        node.pos.x = new_x
        node.pos.y = new_y
        # Update connected components
        for cpt in node.connected:
            cpt.gcpt.undraw()
            cpt.gcpt.draw(self, color=self.preferences.color('line'))

    def node_join(self, from_node, to_node=None):
        """
        Joins all components in node1, to those in node2, then removes node1 from the circuit.

        Parameters
        ----------
        from_node : lcapy.nodes.Node
            The node to merge from
        to_node : lcapy.nodes.Node, optional
            The node to merge onto

        Returns
        -------
        connected_cpts : list[lcapy.mnacpts.Cpt, ...]
            A copy of the list of components that were moved from node2 to node1

        """

        if to_node is None:
            print(f"No node provided, searching for existing node at ({from_node.pos.x}, {from_node.pos.y})") if self.ui.debug else None
            to_node = self.closest_node(from_node.pos.x, from_node.pos.y, ignore=from_node)
        if to_node is None:
            print(f"No existing node found at ({from_node.pos.x}, {from_node.pos.y})") if self.ui.debug else None
            return None
        print(f"Joining {from_node.name} and {to_node.name}") if self.ui.debug else None


        # If the two nodes are the same, disallow. This should not happen.
        if from_node.name == to_node.name:
            warn(f"Tried to merge node {from_node.name} with itself.\n\
                this should not happen, and is likely due to an error.")
            return

        connected_from = []

        # update every component in node1 to be in node2
        for cpt in from_node.connected:
            # store the moved component for return
            connected_from.append(cpt)
            # Remove node1 from the component
            cpt.nodes.remove(from_node)
            # Remove the component from node1
            from_node.remove(cpt)
            # Add the component to node2
            to_node.append(cpt)
            # Add node2 to the component
            cpt.nodes.append(to_node)

        # return information required for history
        return from_node, to_node, connected_from

    def node_split(self, existing_node, new_node=None, components=None):
        """
        moves the given components from node1 to new node2

        Parameters
        ----------
        existing_node
        new_node_name
        components

        Returns
        -------

        """
        # Must pass in components to move
        if components is None or len(components) == 0:
            if self.ui.debug:
                print('No components moved')
            return None
        if new_node is None:
            return
            # TODO: Implement creating a new node if none is passed in
            # new_node = Node(self.circuit, new_node_name)
            # # Add the new node to the circuit
            # self.circuit.nodes[new_node_name] = new_node
            # # Copy the original nodes position
            # new_node.pos = copy(existing_node.pos)

        # Ensure the new node is on the circuit
        self.circuit.nodes[new_node.name] = new_node
        # Copy the original nodes position
        new_node.pos = copy(existing_node.pos)

        # update every component in components to be in new_node
        for cpt in components:
            # Remove the component from existing_node
            existing_node.remove(cpt)
            # Remove existing_node from the component
            cpt.nodes.remove(existing_node)
            # Add the component to new_node
            new_node.append(cpt)
            # Add new_node to the component
            cpt.nodes.append(new_node)

        # return the new node
        return new_node

    def cpt_modify_nodes(self, cpt, x1, y1, x2, y2):

        gcpt = cpt.gcpt
        cpt_key = gcpt.type

        self.cpt_delete(gcpt)
        newcpt = self.cpt_create(cpt_key, x1, y1, x2, y2, gcpt.kind)

        # TODO: tidy
        newgcpt = newcpt.gcpt
        newgcpt.kind = gcpt.kind
        newcpt.args = cpt.args
        newcpt.opts.clear()
        newcpt.opts.add(gcpt.attr_string(newgcpt.node1.x, newgcpt.node1.y,
                                         newgcpt.node2.x, newgcpt.node2.y))

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
                                         gcpt.node2.x, gcpt.node2.y,
                                         self.node_spacing))

        newcpt.gcpt = gcpt
        return newcpt

    def create(self, thing, x1, y1, x2, y2, kind=''):

        cpt = self.cpt_create(thing, x1, y1, x2, y2, kind)
        self.history.append(HistoryEvent('A', cpt))

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

            width = sch.width * self.node_spacing
            height = sch.height * self.node_spacing

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
                gcpt = gcpt_make_from_cpt(cpt)
            except Exception as e:
                gcpt = None
                self.exception(e)

            cpt.gcpt = gcpt

        self.invalidate()
        self.check_drawable_nodes()
        self.redraw()

    def paste(self, x1, y1, x2, y2):

        if self.clipboard is None:
            return

        cpt = self.thing_create(self.clipboard.type, x1, y1, x2, y2,
                                self.clipboard.kind)
        self.history.append(HistoryEvent('A', cpt))
        self.select(cpt)
        return cpt

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

    def rotate(self, cpt, angle=90, midpoint=None):
        """
        Rotates a component by a given angle
        Parameters
        ----------
        cpt : lcapy.mnacpts.Cpt
        angle : float
        midpoint : tuple[float, float] or None
        """
        # convert the angle to radians
        angle = angle * 3.141592654 / 180

        # extract the node coordinates from each node
        p1_x, p1_y = cpt.gcpt.node1.x, cpt.gcpt.node1.y
        p2_x, p2_y = cpt.gcpt.node2.x, cpt.gcpt.node2.y

        # calculate the midpoint
        if midpoint is None:
            mid_x, mid_y = cpt.gcpt.midpoint.xy
        else:
            mid_x, mid_y = self.snap_to_grid(midpoint[0], midpoint[1])

        # Rotate nodes about midpoint
        r1_x = mid_x + cos(angle) * (p1_x - mid_x) - sin(angle) * (p1_y - mid_y)
        r1_y = mid_y + sin(angle) * (p1_x - mid_x) + cos(angle) * (p1_y - mid_y)

        r2_x = mid_x + cos(angle) * (p2_x - mid_x) - sin(angle) * (p2_y - mid_y)
        r2_y = mid_y + sin(angle) * (p2_x - mid_x) + cos(angle) * (p2_y - mid_y)

        # TODO: Fix snapping to not alter length of cpt too much
        # if self.preferences.snap_grid:
        #     r1_x, r1_y = self.snap_to_grid(r1_x, r1_y)
        #     r2_x, r2_y = self.snap_to_grid(r2_x, r2_y)

        # Add rotation to history
        node_positions = [(node.pos.x, node.pos.y) for node in self.selected.nodes]
        new_positions = [(r1_x, r1_y), (r2_x, r2_y)]
        self.history.append(HistoryEvent('M', cpt, node_positions, new_positions))

        # move nodes
        self.node_move(cpt.gcpt.node1, r1_x, r1_y)
        self.node_move(cpt.gcpt.node2, r2_x, r2_y)


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

    def thing_create(self, cpt_type, x1, y1, x2, y2, kind='', join=True):
        """
        Creates a new component of type cpt_type between two points identified by (x1, y1) and (x2, y2).

        :param cpt_type: New component type
        :param float x1:
        :param float y1:
        :param float x2:
        :param float y2:
        :param kind: The kind of component to create
        :return: The instance of the component
        """
        from lcapy.mnacpts import Cpt

        cpt_name = self.choose_cpt_name(cpt_type)
        gcpt = gcpt_make_from_type(cpt_type, cpt_name, kind=kind)
        if gcpt is None:
            return None

        all_node_names = list(self.circuit.nodes)
        node_names = []
        positions = gcpt.assign_positions(x1, y1, x2, y2)

        for m, position in enumerate(positions):
            if position is None:
                continue

            node = self.circuit.nodes.by_position(position)
            if node is None or not join:
                node_name = gcpt.choose_node_name(m, all_node_names)
                all_node_names.append(node_name)
            else:
                node_name = node.name
            node_names.append(node_name)

        netitem = gcpt.netitem(node_names, x1, y1, x2, y2, self.node_spacing)

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

        cpt.gcpt = gcpt

        self.check_drawable_nodes()

        self.cpt_draw(cpt)

        self.select(cpt)

        return cpt

    def check_drawable_nodes(self):

        # FIXME, this is unnecessarily complicated due to Lcapy and
        # Lcapy-gui components both having nodes.

        nodes = self.circuit.nodes

        for node in nodes.values():
            node.is_drawn = True
            node.is_implicit = False

        for cpt in self.circuit.elements.values():
            if not hasattr(cpt, 'gcpt'):
                continue
            gcpt = cpt.gcpt
            gcpt_nodes = set(gcpt.nodes)
            drawn_nodes = set(gcpt.drawn_nodes)

            for node in gcpt_nodes - drawn_nodes:
                # This could be simplified if cpt nodes and gcpt nodes
                # are the same.
                nodes[node.name].is_drawn = False

            for node in gcpt.implicit_nodes:
                node.is_implicit = True

        for cpt in self.circuit.elements.values():
            if not hasattr(cpt, 'gcpt'):
                continue
            gcpt = cpt.gcpt
            for node in gcpt.nodes:
                node.is_drawn = nodes[node.name].is_drawn
                node.is_implicit = nodes[node.name].is_implicit

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

    def snap_to_cpt(self, x, y, cpt):
        """
        Projects the current point onto the nearest component

        Parameters
        ==========
        x : float
            x coordinate of the point to project
        y : float
            y coordinate of the point to project
        cpt : lcapy.mnacpts.Cpt

        Returns
        =======
        tuple[float, float]

        """

        v1_x, v1_y = cpt.gcpt.node1.x, cpt.gcpt.node1.y
        v2_x, v2_y = cpt.gcpt.node2.x, cpt.gcpt.node2.y

        # Convert line to a vector relative to node1
        cpt_vect = array([v2_x - v1_x, v2_y - v1_y])
        # Convert point x,y to a vector relative to node1
        point_vect = array([x - v1_x, y - v1_y])


        #  Project the point x,y onto the line
        dot_product = (dot(point_vect, cpt_vect) / dot(cpt_vect, cpt_vect)) * cpt_vect

        # Convert point vector back to point and return
        return dot_product[0] + v1_x, dot_product[1] + v1_y

    def snap_to_grid_x(self, x):

        snap = self.grid_spacing
        x = floor((x + 0.5 * snap) / snap) * snap
        return x

    def snap_to_grid_y(self, y):

        snap = self.grid_spacing
        y = floor((y + 0.5 * snap) / snap) * snap
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
        ann1.draw(color='red', fontsize=40 * self.zoom_factor)
        ann2.draw(color='blue', fontsize=40 * self.zoom_factor)

    @property
    def ground_node(self):

        return self.node_find('0')

    def node_draw(self, node):

        if node.pos is None:
            print('Pos unknown for ' + str(node))
            return

        if node.port:
            self.ui.sketcher.stroke_donut(
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

        if self.recall == []:
            return
        event = self.recall.pop()
        self.history.append(event)

        if self.ui.debug:
            print('Redo ' + event.code)

        self.apply(event, False)

    def redraw(self):

        for cpt in self.circuit.elements.values():
            if cpt == self.selected:
                self.cpt_draw(cpt, color=self.preferences.color("select"))
            else:
                self.cpt_draw(cpt)

        # Should redraw nodes on top to blank out wires on top of ports

    def undo(self):

        if self.history == []:
            return
        event = self.history.pop()
        self.recall.append(event)

        if self.ui.debug:
            print('Undo ' + event.code)

        self.apply(event, True)

    def undraw(self):

        for cpt in self.circuit.elements.values():
            gcpt = cpt.gcpt
            gcpt.undraw()

    def get_navigate_mode(self):
        """
        Returns the current navigate mode of the canvas

        e.g. ZOOM, PAN, etc.
        """
        return self.ui.canvas.drawing.ax.get_navigate_mode()
