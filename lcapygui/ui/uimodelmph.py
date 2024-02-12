from .cursor import Cursor
from .cursors import Cursors
from .uimodelbase import UIModelBase
from .history_event import HistoryEvent
from lcapy.nodes import Node
from lcapy.mnacpts import Cpt
from lcapy import Circuit
from os.path import basename
from warnings import warn
from numpy import sqrt


class UIModelMPH(UIModelBase):
    def __init__(self, ui):
        """
        Defines the UIModelMPH class
        Parameters
        ==========
        ui : lcapygui.ui.tk.lcapytk.LcapyTk
            tkinter UI interface

        """
        super(UIModelMPH, self).__init__(ui)

        self.last_pos = None
        self.cursors = Cursors()
        self.node_cursor = None

        self.key_bindings = {
            'ctrl+c': self.on_copy,
            'ctrl+d': self.on_debug,
            'ctrl+e': self.on_export,
            'ctrl+h': self.on_help,
            'ctrl+i': self.on_inspect,
            'ctrl+n': self.on_new,
            'ctrl+o': self.on_load,
            'ctrl+s': self.on_save,
            'alt+s': self.on_save_as,
            'ctrl+t': self.on_exchange_cursors,
            'ctrl+u': self.on_view,
            'ctrl+v': self.on_paste,
            'ctrl+w': self.on_quit,
            'ctrl+x': self.on_cut,
            'ctrl+y': self.on_redo,
            'ctrl+z': self.on_undo,
            'ctrl+9': self.on_pdb,
            'escape': self.on_unselect,
            'delete': self.on_delete,
            'backspace': self.on_delete}

        # Handle menu accelerator keys
        self.key_bindings_with_key = {}
        for k, thing in self.component_map.items():
            self.key_bindings_with_key[thing.accelerator] = self.on_add_cpt, thing
        for k, thing in self.connection_map.items():
            self.key_bindings_with_key[thing.accelerator] = self.on_add_con, thing

        if self.first_use:
            self.on_first_launch()
            self.preferences.save()

    def add_cursor(self, x, y):
        """
        Adds a cursor at the specified position.

        Explanation
        ===========
        Adds a cursor at the provided x & y position.
        If two cursors already exist, the oldest cursor is removed.

        The oldest cursor is considered positive, and the newest is considered negative.

        Parameters
        ==========
        x : float
            x position of the cursor
        y : float
            y position of the cursor

        """
        # cursors[0] is the positive cursor
        # cursors[1] is the negative cursor

        cursor = Cursor(self.ui, x, y)

        # If this is the first cursor, add it and make it positive
        if len(self.cursors) == 0:
            cursor.draw('red')
            self.cursors.append(cursor)
        # If there is already a cursor, make the new cursor negative
        elif len(self.cursors) == 1:
            cursor.draw('blue')
            self.cursors.append(cursor)

        elif len(self.cursors) == 2:
            rp = (x - self.cursors[0].x) ** 2 + (y - self.cursors[0].y) ** 2
            rm = (x - self.cursors[1].x) ** 2 + (y - self.cursors[1].y) ** 2

            if rm > rp:
                # Close to plus cursor so add new minus cursor
                self.cursors[1].remove()
                self.cursors[1] = cursor
                self.cursors[1].draw('blue')
            else:
                # Close to minus cursor so change minus cursor to plus cursor
                # and add new minus cursor
                self.cursors[0].remove()
                self.cursors[1].remove()
                self.cursors[0] = self.cursors[1]
                self.cursors[0].draw('red')
                self.cursors[1] = cursor
                self.cursors[1].draw('blue')

        self.ui.refresh()

    def clear(self):

        # TODO: better to remove the drawn artists
        # If don't want grid, use grid(False)

        # This removes the callbacks
        self.ui.clear(self.preferences.grid)

        ax = self.ui.canvas.drawing.ax
        ax.callbacks.connect('xlim_changed', self.on_mouse_zoom)
        ax.callbacks.connect('ylim_changed', self.on_mouse_zoom)

    def closest_cpt(self, x, y):
        """
        Returns the component closest to the specified position

        Parameters
        ==========
        x : float
            x position
        y : float
            y position

        Returns
        =======
        cpt: lcapy.mnacpts.Cpt or None
            the closest component to (x,y) or None if no component is close
        """
        for cpt in self.circuit.elements.values():
            gcpt = cpt.gcpt
            if gcpt is None:
                continue

            if gcpt.is_within_bbox(x, y):
                return cpt

        return None

    def closest_node(self, x, y, ignore=None):
        """
        Returns the node closest to the specified position

        Parameters
        ----------
        x : float
            x position
        y : float
            y position
        ignore : lcapy.nodes.Node or list[lcapy.nodes.Node, ...], optional
            Node(s) to ignore

        """

        if type(ignore) == Node:
            ignore = [ignore]


        for node in self.circuit.nodes.values():
            if node.pos is None:
                # This happens with opamps.  Node 0 is the default
                # reference pin.
                warn('Ignoring node %s with no position' % node.name)
                continue
            elif ignore is not None and node in ignore:
                if self.ui.debug:
                    print('Ignoring node %s' % node.name)
                continue
            x1, y1 = node.pos.x, node.pos.y
            rsq = (x1 - x) ** 2 + (y1 - y) ** 2
            if rsq < 0.1:
                return node
        return None

    def create_state_space(self, cpt):
        """
        TODO: Correct Docstring

        Parameters
        ==========
        cpt : lcapy.mnacpts.Cpt
            Component to create state space for

        """
        ss = self.circuit.ss
        self.ui.show_state_space_dialog(ss)

    def create_transfer_function(self, cpt):
        """
        Shows the transfer function for the component 'cpt'

        Parameters
        ==========
        cpt : lcapy.mnacpts.Cpt
            Component to create transfer function for

        """
        self.ui.show_transfer_function_dialog(cpt)

    def create_twoport(self, cpt, kind):
        """
        TODO: add docstring

        Parameters
        ==========
        cpt : lcapy.mnacpts.Cpt
            Component to create twoport for
        kind : str
            String key for the twoport type

        """
        self.ui.show_twoport_dialog(cpt, kind)

    def exception(self, e):
        """
        Shows an error dialog with exception message 'e'

        Parameters
        ==========
        e : Exception

        """
        message = str(e)
        if self.pathname != '':
            message += ' in ' + self.pathname
        if self.ui.debug:
            breakpoint()
        self.ui.show_error_dialog(message)

    def new_name(self, pathname):
        """
        # TODO: what does this do?

        Parameters
        ==========
        pathname : str
            Pathname of the file to create

        Returns
        =======
        str
            New pathname
        """
        from os.path import splitext

        base, ext = splitext(pathname)
        parts = base.split('_')
        if len(parts) == 0:
            suffix = '1'
        else:
            try:
                suffix = str(int(parts[-1]) + 1)
                base = '_'.join(parts[0:-1])
            except ValueError:
                suffix = '1'
        return base + '_' + suffix + ext

    def on_ac_model(self):
        """
        Changes the circuit to an AC model

        """
        # Perhaps should kill non-AC sources
        cct = self.circuit.ac()
        self.on_show_new_circuit(cct)

    def on_add_node(self, x, y):

        x, y = self.snap(x, y)

        self.add_cursor(x, y)

    def on_add_cpt(self, thing):

        if self.ui.debug:
            print(thing.cpt_type)

        if len(self.cursors) == 0:
            self.ui.show_info_dialog(
                'To add component, first create nodes by clicking on grid')
            return
        elif len(self.cursors) == 1:
            self.ui.show_info_dialog(
                'To add component, add negative node by clicking on grid')
            return

        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        self.create(thing.cpt_type, x1, y1, x2, y2)
        self.ui.refresh()

    def on_add_con(self, thing):

        if self.ui.debug:
            print(thing.cpt_type)

        if len(self.cursors) == 0:
            self.ui.show_info_dialog(
                'To add component, first create nodes by clicking on grid')
            return
        elif len(self.cursors) == 1:
            self.ui.show_info_dialog(
                'To add component, add negative node by clicking on grid')
            return

        # TODO: if have a single cursor choose down direction.

        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        self.create(thing.cpt_type, x1, y1, x2, y2, kind='-' + thing.kind)
        self.ui.refresh()

    def on_best_fit(self):

        bbox = self.bounding_box()
        if bbox is None:
            return
        xmin, ymin, xmax, ymax = bbox

        self.ui.set_view(xmin - 2, ymin - 2, xmax + 2, ymax + 2)
        self.ui.refresh()

    def on_clone(self):

        pathname = self.new_name(self.pathname)
        self.save(pathname)

        model = self.ui.new()
        model.load(pathname)
        filename = basename(pathname)
        self.ui.set_filename(filename)
        self.ui.refresh()

    def on_close(self):
        """
        Close the lcapy-gui window

        """

        self.ui.quit()

    def on_copy(self):
        """
        Copy the selected component

        """
        if self.selected is None:
            return
        if not self.cpt_selected:
            return

        self.copy(self.selected)

    def on_cpt_changed(self, cpt):

        self.invalidate()
        # Component name may have changed
        self.clear()

        if isinstance(cpt, Cpt):

            # If kind has changed need to remake the sketch
            # and remake the cpt.
            # If name changed need to remake the cpt.
            self.cpt_remake(cpt)
        else:
            # Node name may have changed...
            pass

        self.redraw()
        self.cursors.draw()
        self.ui.refresh()

    def on_create_state_space(self):

        self.create_state_space(self.selected)

    def on_create_transfer_function(self):

        self.create_transfer_function(self.selected)

    def on_create_twoport(self, kind):

        self.create_twoport(self.selected, kind)

    def on_cut(self):

        if self.selected is None:
            return
        if not self.cpt_selected:
            return

        self.cut(self.selected)

        self.cursors.draw()

        self.ui.refresh()

    def on_dc_model(self):

        # Perhaps should kill non-DC sources
        cct = self.circuit.dc()
        self.on_show_new_circuit(cct)

    def on_debug(self):

        s = ''
        s += 'Netlist.........\n'
        s += self.schematic() + '\n'
        s += 'Nodes...........\n'
        s += self.circuit.nodes.debug() + '\n'
        s += 'Cursors.........\n'
        s += self.cursors.debug() + '\n'
        s += 'Selected.........\n'
        s += str(self.selected) + '\n'
        s += '\nHistory.........\n'
        s += str(self.history) + '\n'
        s += '\nRecall.........\n'
        s += str(self.recall)
        self.ui.show_message_dialog(s, 'Debug')

    def on_delete(self):
        """
        If a component is selected, delete it, then redraw and refresh the UI

        """

        if self.selected is None:
            return
        if not self.cpt_selected:
            # Handle node deletion later
            return

        self.delete(self.selected)

        self.cursors.draw()

        self.ui.refresh()

    def on_describe(self):

        self.ui.show_message_dialog(self.circuit.description(),
                                    title='Description')

    def on_exchange_cursors(self):

        self.exchange_cursors()

    def on_expand(self):

        cct = self.circuit.expand()
        self.on_show_new_circuit(cct)

    def on_export(self):

        pathname = self.ui.export_file_dialog(self.pathname)
        if pathname == '':
            return
        self.export(pathname)

    def on_expression(self):

        from lcapy import expr

        e = self.last_expr if self.last_expr is not None else expr(0)
        self.ui.show_expr_dialog(e)

    def on_help(self):

        self.ui.show_help_dialog()

    def on_inspect(self):

        if not self.selected:
            return

        if not self.cpt_selected:
            return

        self.ui.show_inspect_dialog(self.selected,
                                    title=self.selected.name)

    def on_inspect_properties(self):
        if self.cpt_selected:
            self.ui.inspect_properties_dialog(self.selected,
                                              self.on_cpt_changed,
                                              title=self.selected.name)
        else:
            self.ui.show_node_properties_dialog(self.selected,
                                                self.on_cpt_changed,
                                                title='Node ' +
                                                self.selected.name)

    def on_inspect_current(self, cpt=None):

        if cpt is None:
            if not self.selected or not self.cpt_selected:
                return
            cpt = self.selected

        win = self.ui.show_working_dialog('Calculating voltage')
        self.inspect_current(cpt)
        win.destroy()

    def on_inspect_noise_current(self):

        if not self.selected or not self.cpt_selected:
            return

        win = self.ui.show_working_dialog('Calculating noise current')
        self.inspect_noise_current(self.selected)
        win.destroy()

    def on_inspect_noise_voltage(self):

        if not self.selected or not self.cpt_selected:
            return

        win = self.ui.show_working_dialog('Calculating noise voltage')
        self.inspect_noise_voltage(self.selected)
        win.destroy()

    def on_inspect_norton_admittance(self, cpt=None):

        if cpt is None:
            if not self.selected or not self.cpt_selected:
                return
            cpt = self.selected

        if not self.selected or not self.cpt_selected:
            return

        self.inspect_norton_admittance(cpt)

    def on_inspect_thevenin_impedance(self, cpt=None):

        if cpt is None:
            if not self.selected or not self.cpt_selected:
                return
            cpt = self.selected

        self.inspect_thevenin_impedance(cpt)

    def on_inspect_voltage(self, cpt=None):

        if cpt is None:
            if not self.selected or not self.cpt_selected:
                return
            cpt = self.selected
        win = self.ui.show_working_dialog('Calculating voltage')
        self.inspect_voltage(cpt)
        win.destroy()

    def on_laplace_model(self):

        cct = self.circuit.s_model()
        self.on_show_new_circuit(cct)

    def on_left_click(self, x, y):

        self.on_select(x, y)

        if self.cpt_selected:
            cpt = self.selected
            if self.ui.debug:
                print('Selected ' + cpt.name)
            self.cursors.remove()
            self.add_cursor(cpt.gcpt.node1.pos.x, cpt.gcpt.node1.pos.y)
            node2 = cpt.gcpt.node2
            if node2 is not None:
                self.add_cursor(node2.pos.x, node2.pos.y)
        else:
            if self.ui.debug:
                print('Add node at (%s, %s)' % (x, y))
            self.on_add_node(x, y)

    def on_left_double_click(self, x, y):

        self.on_right_click(x, y)

    def on_load(self, initial_dir='.'):

        pathname = self.ui.open_file_dialog(initial_dir)
        if pathname == '' or pathname == ():
            return

        model = self.ui.new()
        model.load(pathname)
        self.ui.set_filename(pathname)
        self.ui.refresh()

    def on_manipulate_kill(self):

        # Could have a dialog to select what to kill

        cct = self.circuit.kill()
        self.on_show_new_circuit(cct)

    def on_manipulate_remove_sources(self):

        # Could have a dialog to select what to remove

        # Remove independent sources
        cct = self.circuit.copy()
        cct = cct.copy()
        values = list(cct.elements.values())
        for cpt in values:
            if cpt.is_independent_source:
                cct.remove(cpt.name)

        self.on_show_new_circuit(cct)

    def on_mesh_equations(self):

        try:
            la = self.circuit.loop_analysis()
        except Exception as e:
            self.exception(e)
            return

        eqns = la.mesh_equations()
        self.ui.show_equations_dialog(eqns, 'Mesh equations')

    def on_mouse_drag(self, x, y, key):

        # Perhaps allow multiple cpts to be selected at once for dragging?

        if self.ui.debug:
            print('mouse drag')

        if not self.selected or not self.cpt_selected:
            return
        cpt = self.selected

        if not self.dragged:
            self.dragged = True
            x0, y0 = self.select_pos
            x0, y0 = self.snap(x0, y0)
            self.last_pos = x0, y0
            self.node_positions = [(node.pos.x, node.pos.y)
                                   for node in cpt.nodes]

        x0, y0 = self.last_pos

        x, y = self.snap(x, y)
        self.last_pos = x, y

        xshift = x - x0
        yshift = y - y0

        self.cpt_move(cpt, xshift, yshift, key == 'shift')
        self.ui.refresh()

    def on_mouse_release(self, key=None):

        if self.ui.debug:
            print('mouse release')

        if not self.dragged:
            return

        if not self.selected or not self.cpt_selected:
            return
        cpt = self.selected

        self.dragged = False
        node_positions = [(node.pos.x, node.pos.y)
                          for node in cpt.nodes]
        self.history.append(HistoryEvent('M', cpt, self.node_positions,
                                         node_positions))

        # The following is only required to fix up the label
        self.redraw()
        self.ui.refresh()

    def on_mouse_zoom(self, ax):
        """This is called whenever xlim or ylim changes; usually
        in response to selecting area with the mouse to zoom."""

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        r = sqrt((xlim[1] - xlim[0])**2 + (ylim[1] - ylim[0])**2)

        xsize = self.preferences.xsize
        ysize = self.preferences.ysize
        R = sqrt(xsize**2 + ysize**2)
        self.zoom_factor = R / r

        if self.ui.debug:
            print('zoom %s' % self.zoom_factor)

        self.clear()
        self.redraw()

        # Don't refresh; will keep the old axes size
        # self.ui.refresh()

    def on_simple_netlist(self):

        netlist = []
        lines = self.circuit.netlist().split('\n')
        for line in lines:
            parts = line.split(';')
            netlist.append(parts[0].strip())
        s = '\n'.join(netlist)
        self.ui.show_message_dialog(s, 'Netlist')

    def on_netlist(self):

        s = self.schematic()
        self.ui.show_message_dialog(s, 'Netlist')

    def on_modified_nodal_equations(self):

        cct = self.analysis_circuit
        cct = cct.laplace()
        eqns = cct.matrix_equations()
        # Perhaps have matrix equation dialog?
        self.ui.show_expr_dialog(eqns, 'Modified nodal equations')

    def on_nodal_equations(self):

        try:
            na = self.circuit.nodal_analysis(node_prefix='n')
        except Exception as e:
            self.exception(e)
            return

        eqns = na.nodal_equations()
        self.ui.show_equations_dialog(eqns, 'Nodal equations')

    def on_new(self):

        self.ui.new()

    def on_noise_model(self):

        cct = self.circuit.noise_model()
        self.on_show_new_circuit(cct)

    def on_paste(self):

        if len(self.cursors) < 2:
            # TODO, place cpt where mouse is...
            return
        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        self.paste(x1, y1, x2, y2)
        self.ui.refresh()

    def on_pdb(self):

        import pdb
        pdb.set_trace()

    def on_preferences(self):

        def update():
            self.on_redraw()
            # Handle current_sign_convention
            self.invalidate()
            self.preferences.apply()

        self.ui.show_preferences_dialog(update)

    def on_first_launch(self):
        self.ui.show_first_launch_dialog()

    def on_quit(self):

        if self.dirty:
            self.ui.show_info_dialog('Schematic not saved')
        else:
            self.ui.quit()

    def on_redo(self):

        self.redo()
        self.ui.refresh()

    def on_redraw(self):

        self.clear()
        self.redraw()
        self.ui.refresh()

    def on_resize(self):

        if self.ui.debug:
            print('resize')

        # TODO:  fix up canvas size when maximize the window

    def on_right_click(self, x, y):

        self.on_select(x, y)
        if not self.selected:
            return

        self.on_inspect_properties()

    def on_right_double_click(self, x, y):
        pass

    def on_rotate(self, angle):

        self.rotate(angle)

    def on_save(self):

        pathname = self.pathname
        if pathname == '':
            return
        self.save(pathname)
        self.ui.save(pathname)

    def on_save_as(self):

        pathname = self.ui.save_file_dialog(self.pathname)
        if pathname == '' or pathname == ():
            return
        self.save(pathname)
        self.ui.save(pathname)

    def on_screenshot(self):

        pathname = self.ui.export_file_dialog(self.pathname,
                                              default_ext='.png')
        if pathname == '' or pathname == ():
            return
        self.ui.screenshot(pathname)

    def on_select(self, x, y):

        self.select_pos = x, y

        node = self.closest_node(x, y)
        cpt = None
        if node is None:
            cpt = self.closest_cpt(x, y)

        if cpt:
            self.select(cpt)
            # TODO: only redraw selected component
            # Redraw to highlight selected component
            self.on_redraw()
        elif node:
            self.select(node)
        else:
            self.select(None)

    def on_show_new_circuit(self, cct):

        model = self.ui.new()
        model.load_from_circuit(cct)

        pathname = self.new_name(self.pathname)
        filename = basename(pathname)
        self.ui.set_filename(filename)
        self.ui.refresh()

    def on_transient_model(self):

        # Perhaps should kill non-transient sources
        cct = self.circuit.transient()
        self.on_show_new_circuit(cct)

    def on_undo(self):

        self.undo()
        self.ui.refresh()

    def on_unselect(self):

        self.unselect()

    def on_view(self):

        self.view()

    def on_view_macros(self):

        from lcapy.system import tmpfilename
        from os import remove

        schtex_filename = tmpfilename('.schtex')

        cct = Circuit(self.schematic())
        cct.draw(schtex_filename)

        with open(schtex_filename) as f:
            content = f.read()
        remove(schtex_filename)

        self.ui.show_message_dialog(content)

    def exchange_cursors(self):

        if len(self.cursors) < 2:
            return
        self.cursors[0], self.cursors[1] = self.cursors[1], self.cursors[0]
        self.cursors[0].remove()
        self.cursors[1].remove()
        self.cursors[0].draw('red')
        self.cursors[0].draw('red')
        self.cursors[1].draw('blue')
        self.ui.refresh()

    def unselect(self):

        self.selected = None
        self.cursors.remove()
        self.redraw()
        self.ui.refresh()
