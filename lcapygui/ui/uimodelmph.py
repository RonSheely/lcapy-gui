from .uimodelbase import UIModelBase
from ..components.cpt_maker import cpt_remake
from ..components.component import Component


class Cursor:

    def __init__(self, ui, x, y):

        self.layer = ui.layer
        self.patch = None
        self.x = x
        self.y = y

    @property
    def position(self):

        return self.x, self.y

    def draw(self, color='red', radius=0.3):

        self.patch = self.layer.stroke_filled_circle(self.x, self.y,
                                                     radius,
                                                     color=color,
                                                     alpha=0.5)

    def remove(self):

        self.patch.remove()


class Cursors(list):

    def debug(self):

        s = ''
        for cursor in self:
            s += '%s, %s' % (cursor.x, cursor.y) + '\n'
        return s

    def remove(self):

        while self != []:
            self.pop().remove()

    def draw(self):

        if len(self) > 0:
            self[0].draw('red')
        if len(self) > 1:
            self[1].draw('blue')


class UIModelMPH(UIModelBase):

    def __init__(self, ui):

        super(UIModelMPH, self).__init__(ui)

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

        self.key_bindings_with_key = {
            '0': self.on_add_con,
            'c': self.on_add_cpt,
            'd': self.on_add_cpt,
            'e': self.on_add_cpt,
            'f': self.on_add_cpt,
            'g': self.on_add_cpt,
            'h': self.on_add_cpt,
            'i': self.on_add_cpt,
            'l': self.on_add_cpt,
            'o': self.on_add_cpt,
            'p': self.on_add_cpt,
            'r': self.on_add_cpt,
            'v': self.on_add_cpt,
            'w': self.on_add_cpt}

    def add_cursor(self, x, y):

        x, y = self.snap(x, y)

        cursor = Cursor(self.ui, x, y)

        if len(self.cursors) == 0:
            cursor.draw('red')
            self.cursors.append(cursor)

        elif len(self.cursors) == 1:
            cursor.draw('blue')
            self.cursors.append(cursor)

        elif len(self.cursors) == 2:

            rp = (x - self.cursors[0].x)**2 + (y - self.cursors[0].y)**2
            rm = (x - self.cursors[1].x)**2 + (y - self.cursors[1].y)**2

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

        self.ui.clear(self.preferences.grid)

    def draw_node_select(self, x, y):

        x, y = self.snap(x, y)

        if self.node_cursor is not None:
            self.node_cursor.remove()

        cursor = Cursor(self.ui, x, y)
        cursor.draw('black', 0.2)
        self.node_cursor = cursor
        self.ui.refresh()

    def exception(self, message):
        self.ui.show_error_dialog(message)

    def unselect(self):

        self.cursors.remove()
        self.ui.refresh()

    def on_add_node(self, x, y):

        self.add_cursor(x, y)

    def on_add_cpt(self, cpt_key):

        if self.ui.debug:
            print(cpt_key)

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

        self.cpt_create(cpt_key, x1, y1, x2, y2)
        self.ui.refresh()

    def on_add_con(self, con_key):

        if self.ui.debug:
            print(con_key)

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

        self.con_create(con_key, x1, y1, x2, y2)
        self.ui.refresh()

    def on_best_fit(self):

        bbox = self.bounding_box()
        if bbox is None:
            return
        xmin, ymin, xmax, ymax = bbox

        self.ui.set_view(xmin - 1, ymin - 1, xmax + 1, ymax + 1)
        self.ui.refresh()

    def on_close(self):

        self.ui.quit()

    def on_copy(self):

        pass

    def on_cpt_changed(self, cpt):

        self.invalidate()
        # Component name may have changed
        self.clear()
        if isinstance(cpt, Component):
            # If kind has changed need to remake the sketch
            cpt_remake(cpt)
        self.redraw()
        self.ui.refresh()

    def on_debug(self):

        s = ''
        s += 'Netlist.........\n'
        s += self.schematic() + '\n'
        s += 'Nodes...........\n'
        s += self.nodes.debug() + '\n'
        s += 'Cursors.........\n'
        s += self.cursors.debug() + '\n'
        s += 'Selected.........\n'
        s += str(self.selected) + '\n'
        self.ui.show_message_dialog(s, 'Debug')

    def on_cut(self):

        if self.selected is None:
            return
        if not self.cpt_selected:
            return

        self.cut(self.selected)

        self.cursors.draw()

        self.ui.refresh()

    def on_delete(self):

        if self.selected is None:
            return
        if not self.cpt_selected:
            # Handle node deletion later
            return

        self.delete(self.selected)

        self.cursors.draw()

        self.ui.refresh()

    def on_describe(self):

        self.ui.show_message_dialog(self.cct.description(),
                                    title='Description')

    def on_export(self):

        filename = self.ui.export_file_dialog(self.filename)
        if filename == '':
            return
        self.export(filename)

    def on_help(self):

        self.ui.show_help_dialog()

    def on_inspect(self):

        if not self.selected:
            return

        if not self.cpt_selected:
            return

        self.ui.show_inspect_dialog(self.selected,
                                    title=self.selected.name)

    def on_inspect_current(self):

        if not self.selected or not self.cpt_selected:
            return

        self.inspect_current(self.selected)

    def on_inspect_norton_admittance(self):

        if not self.selected or not self.cpt_selected:
            return

        self.inspect_norton_admittance(self.selected)

    def on_inspect_thevenin_impedance(self):

        if not self.selected or not self.cpt_selected:
            return

        self.inspect_thevenin_impedance(self.selected)

    def on_inspect_voltage(self):

        if not self.selected or not self.cpt_selected:
            return

        self.inspect_voltage(self.selected)

    def on_laplace_model(self):

        cct = self.cct.s_model()
        self.on_show_new_circuit(cct)

    def on_left_click(self, x, y):

        self.on_select(x, y)

        if self.cpt_selected:
            cpt = self.selected
            if self.ui.debug:
                print('Selected ' + cpt.name)
            self.cursors.remove()
            self.add_cursor(*cpt.nodes[0].position)
            self.add_cursor(*cpt.nodes[-1].position)
        else:
            if self.ui.debug:
                print('Add node at (%s, %s)' % (x, y))
            self.on_add_node(x, y)

    def on_left_double_click(self, x, y):

        self.on_right_click(x, y)

    def on_load(self):

        filename = self.ui.open_file_dialog()
        if filename == '' or filename == ():
            return

        model = self.ui.new()
        model.load(filename)
        self.ui.set_filename(filename)
        self.ui.refresh()

    def on_mesh_equations(self):

        if self.ground_node is None:
            self.ui.show_info_dialog('Suggest adding a ground node.')

        try:
            la = self.cct.loop_analysis()
        except Exception as e:
            self.exception(e)
            return

        eqns = la.mesh_equations()
        self.ui.show_equations_dialog(eqns, 'Mesh equations')

    def on_move(self, xshift, yshift):

        self.move(xshift, yshift)

    def on_netlist(self):

        netlist = []
        lines = self.cct.netlist().split('\n')
        for line in lines:
            parts = line.split(';')
            netlist.append(parts[0].strip())
        s = '\n'.join(netlist)
        self.ui.show_message_dialog(s, 'Netlist')

    def on_nodal_equations(self):

        if self.ground_node is None:
            self.ui.show_info_dialog('Suggest adding a ground node.')

        try:
            na = self.cct.nodal_analysis()
        except Exception as e:
            self.exception(e)
            return

        eqns = na.nodal_equations()
        self.ui.show_equations_dialog(eqns, 'Nodal equations')

    def on_new(self):

        self.ui.new()

    def on_noise_model(self):

        cct = self.cct.noise_model()
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

        self.ui.show_preferences_dialog(self.on_redraw)

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

    def on_right_click(self, x, y):

        self.on_select(x, y)
        if not self.selected:
            return

        if self.cpt_selected:
            self.ui.inspect_properties_dialog(self.selected,
                                              self.on_cpt_changed,
                                              title=self.selected.name)
        else:
            self.ui.show_node_properties_dialog(self.selected,
                                                self.on_cpt_changed,
                                                title='Node ' +
                                                self.selected.name)

    def on_right_double_click(self, x, y):
        pass

    def on_rotate(self, angle):

        self.rotate(angle)

    def on_save(self):

        filename = self.filename
        if filename == '':
            return
        self.save(filename)
        self.ui.save(filename)

    def on_save_as(self):

        filename = self.ui.save_file_dialog(self.filename)
        if filename == '' or filename == ():
            return
        self.save(filename)
        self.ui.save(filename)

    def on_screenshot(self):

        filename = self.ui.export_file_dialog(self.filename,
                                              default_ext='.png')
        if filename == '' or filename == ():
            return
        self.ui.screenshot(filename)

    def on_select(self, x, y):

        cpt = self.components.closest(x, y)
        node = self.nodes.closest(x, y)

        if cpt and node:
            self.ui.show_error_dialog(
                'Selected both node %s and cpt %s' % (node, cpt))
            return

        if cpt:
            self.select(cpt)
        elif node:
            self.select(node)
        else:
            self.select(None)

    def on_show_new_circuit(self, cct):

        model = self.ui.new()
        model.load_from_circuit(cct)

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
        cct = self.cct
        cct.draw(schtex_filename)

        with open(schtex_filename) as f:
            content = f.read()
        remove(schtex_filename)

        self.ui.show_message_dialog(content)
