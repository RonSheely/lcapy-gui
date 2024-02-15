from tkinter import Canvas, Tk, Frame, TOP, BOTH, BOTTOM, X, PhotoImage
from tkinter.ttk import Notebook, Style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from os.path import basename
from ..uimodeldnd import UIModelDnD
from .sketcher import Sketcher
from .drawing import Drawing
from .menu import MenuBar, MenuDropdown, MenuItem, MenuSeparator
from ...sketch_library import SketchLibrary


class LcapyTk(Tk):
    SCALE = 0.01

    GEOMETRY = '1200x800'
    # Note, need to reduce height from 8 to 7.2 to fit toolbar.
    FIGSIZE = (12, 7.2)
    # FIGSIZE = (6.6, 4)

    NAME = 'lcapy-tk'

    def __init__(self, pathnames=None, debug=0, level=0, icon=None, title="lcapy-gui"):
        from ... import __version__

        super().__init__()

        self.debug = debug
        self.version = __version__
        self.model = None
        self.canvas = None
        self.sketchlib = SketchLibrary()
        self.dialogs = {}

        # Icons and Theming

        if icon is not None:
            icon = PhotoImage(file=icon)
            self.wm_iconphoto(False, icon)

        uimodel_class = UIModelDnD

        self.uimodel_class = uimodel_class

        if self.debug:
            print('model: ', self.uimodel_class)

        # Title and size of the window
        self.title(title + " " + __version__)
        self.geometry(self.GEOMETRY)

        self.level = level

        categories = {
            'Basic': ('c', 'i', 'l', 'p', 'r', 'v', 'w', 'tf'),
            'Opamp': ('opamp', 'fdopamp', 'inamp'),
            'Transistor': ('q', 'j', 'm'),
            'Dependent source': ('e', 'f', 'g', 'h'),
            'Misc.': ('y', 'cpe', 'z', 'o', 'nr', 'switch'),
            'Connection': ('0V', 'ground', 'sground', 'rground', 'cground',
                           'vdd', 'vss', 'vcc', 'vee',
                           'input', 'output', 'bidir')
        }

        items = []
        for cat in categories:
            if cat == 'Basic':
                # The Basic category does not have sub-menus
                for key in categories[cat]:
                    thing = self.uimodel_class.component_map[key]
                    acc = thing.accelerator
                    items.append(MenuItem(thing.menu_name,
                                          command=self.on_add_cpt,
                                          arg=thing, accelerator=acc))
                items.append(MenuSeparator())
            else:
                subitems = []

                for key in categories[cat]:
                    if cat == 'Connection':
                        thing = self.uimodel_class.connection_map[key]
                        cmd = self.on_add_con
                    else:
                        thing = self.uimodel_class.component_map[key]
                        cmd = self.on_add_cpt
                    acc = thing.accelerator
                    subitems.append(MenuItem(thing.menu_name, command=cmd,
                                             arg=thing, accelerator=acc))
                menu = MenuDropdown(cat, 0, subitems)
                items.append(menu)

        component_menu_dropdown = MenuDropdown('Components', 0, items)

        self.menu_parts = {}
        # define menu parts in a dictionary
        self.menu_parts["file_clone"] = MenuItem('Clone', self.on_clone)
        self.menu_parts["file_new"] = MenuItem('New', self.on_new, accelerator='Ctrl+n')
        self.menu_parts["file_open"] = MenuItem('Open', self.on_load, accelerator='Ctrl+o')
        self.menu_parts["file_open_library"] = MenuItem('Open library', self.on_library, underline=6, accelerator='Ctrl+l')
        self.menu_parts["file_save"] = MenuItem('Save', self.on_save, accelerator='Ctrl+s')
        self.menu_parts["file_save_as"] = MenuItem('Save as', self.on_save_as, underline=1, accelerator='Alt+s')
        self.menu_parts["file_export"] = MenuItem('Export', self.on_export, accelerator='Ctrl+e')
        self.menu_parts["screenshot"] = MenuItem('Screenshot', self.on_screenshot, underline=1)
        self.menu_parts["program_quit"] = MenuItem('Quit', self.on_quit, accelerator='Ctrl+q')
        self.menu_parts["preferences"] = MenuItem('Preferences', self.on_preferences)
        self.menu_parts["edit_undo"] = MenuItem('Undo', self.on_undo, accelerator='Ctrl+z')
        self.menu_parts["edit_redo"] = MenuItem('Redo', self.on_redo, accelerator='Ctrl+y')
        self.menu_parts["edit_cut"] = MenuItem('Cut', self.on_cut, accelerator='Ctrl+x')
        self.menu_parts["edit_copy"] = MenuItem('Copy', self.on_copy, accelerator='Ctrl+c')
        self.menu_parts["edit_paste"] = MenuItem('Paste', self.on_paste, accelerator='Ctrl+v')
        self.menu_parts["edit_delete"] = MenuItem('Delete', self.on_delete, accelerator='Del')
        self.menu_parts["edit_values"] = MenuItem('Values', self.on_edit_values, accelerator='Ctrl+V')
        self.menu_parts["view_expression"] = MenuItem('Expression', self.on_expression, accelerator='Ctrl+e')
        self.menu_parts["view_circuitikz_image"] = MenuItem('Circuitikz image', self.on_view, accelerator='Ctrl+u')
        self.menu_parts["view_circuitikz_macros"] = MenuItem('Circuitikz macros', self.on_view_macros)
        self.menu_parts["view_netlist_simple"] = MenuItem('Simple netlist', self.on_simple_netlist)
        self.menu_parts["view_netlist"] = MenuItem('Netlist', self.on_netlist)
        self.menu_parts["view_nodal_equations"] = MenuItem('Nodal equations', self.on_nodal_equations)
        self.menu_parts["view_nodal_equations_modified"] = MenuItem('Modified nodal equations', self.on_modified_nodal_equations)
        self.menu_parts["view_mesh_equations"] = MenuItem('Mesh equations', self.on_mesh_equations)
        self.menu_parts["view_fit_best"] = MenuItem('Best fit', self.on_best_fit)
        self.menu_parts["view_fit_default"] = MenuItem('Default fit', self.on_default_fit)
        self.menu_parts["view_plots"] = MenuItem('Plots', self.on_plots)
        self.menu_parts["view_description"] = MenuItem('Description', self.on_description)
        self.menu_parts["view_annotation"] = MenuItem('Annotation', self.on_annotation)
        self.menu_parts["view_graph_circuit"] = MenuItem('Circuit graph ', self.on_circuitgraph)
        self.menu_parts["create_state_space"] = MenuItem('State space', self.on_create_state_space)
        self.menu_parts["create_transfer_function"] = MenuItem('Transfer function', self.on_create_transfer_function)
        self.menu_parts["create_twoport_a"] = MenuItem('A twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_b"] = MenuItem('B twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_g"] = MenuItem('G twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_h"] = MenuItem('H twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_s"] = MenuItem('S twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_t"] = MenuItem('T twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_y"] = MenuItem('Y twoport', self.on_create_twoport)
        self.menu_parts["create_twoport_z"] = MenuItem('Z twoport', self.on_create_twoport)
        self.menu_parts["inspect_properties"] = MenuItem('Properties', self.on_inspect_properties)
        self.menu_parts["inspect_voltage"] = MenuItem('Voltage', self.on_inspect_voltage)
        self.menu_parts["inspect_current"] = MenuItem('Current', self.on_inspect_current)
        self.menu_parts["inspect_thevenin_impedence"] = MenuItem('Thevenin impedance', self.on_inspect_thevenin_impedance)
        self.menu_parts["inspect_norton_admittance"] = MenuItem('Norton admittance', self.on_inspect_norton_admittance)
        self.menu_parts["inspect_noise_voltage"] = MenuItem('Noise voltage', self.on_inspect_noise_voltage)
        self.menu_parts["inspect_noise_current"] = MenuItem('Noise current', self.on_inspect_noise_current)
        self.menu_parts["manipulate_independent_sources_kill"] = MenuItem('Kill independent sources', self.on_manipulate_kill)
        self.menu_parts["manipulate_independent_sources_remove"] = MenuItem('Remove independent sources', self.on_manipulate_remove_sources)
        self.menu_parts["manipulate_model_ac"] = MenuItem('AC model', self.on_ac_model)
        self.menu_parts["manipulate_model_dc"] = MenuItem('DC model', self.on_dc_model)
        self.menu_parts["manipulate_model_transient"] = MenuItem('Transient model', self.on_transient_model)
        self.menu_parts["manipulate_model_laplace"] = MenuItem('Laplace model', self.on_laplace_model)
        self.menu_parts["manipulate_model_noise"] = MenuItem('Noise model', self.on_noise_model)
        self.menu_parts["manupulate_expand_components"] = MenuItem('Expand components', self.on_expand)
        self.menu_parts["launch_documentation"] = MenuItem('Documentation (default browser)', self.launch_documentation)
        self.menu_parts["help"] = MenuItem('Help', self.on_help, accelerator='Ctrl+h')
        self.menu_parts["help_debug"] = MenuItem('Debug', self.on_debug, accelerator='Ctrl+d')
        self.menu_parts["on_node_join"] = MenuItem('Join Nodes', self.on_node_join)
        self.menu_parts["on_node_split"] = MenuItem('Split Nodes', self.on_node_split)

        # Define menu dropdowns
        self.menu_parts["dropdown_file_menu"] = MenuDropdown('File', 0, [
            self.menu_parts["file_clone"],
            self.menu_parts["file_new"],
            self.menu_parts["file_open"],
            self.menu_parts["file_open_library"],
            self.menu_parts["file_save"],
            self.menu_parts["file_save_as"],
            self.menu_parts["file_export"],
            self.menu_parts["screenshot"],
            self.menu_parts["program_quit"]
        ])
        self.menu_parts["dropdown_edit_menu"] = MenuDropdown('Edit', 0, [
            self.menu_parts["preferences"],
            self.menu_parts["edit_undo"],
            self.menu_parts["edit_redo"],
            self.menu_parts["edit_cut"],
            self.menu_parts["edit_copy"],
            self.menu_parts["edit_paste"],
            self.menu_parts["edit_values"]
        ])
        self.menu_parts["dropdown_view_menu"] = MenuDropdown('View', 0, [
            self.menu_parts["view_expression"],
            self.menu_parts["view_circuitikz_image"],
            self.menu_parts["view_circuitikz_macros"],
            self.menu_parts["view_netlist_simple"],
            self.menu_parts["view_netlist"],
            self.menu_parts["view_nodal_equations"],
            self.menu_parts["view_nodal_equations_modified"],
            self.menu_parts["view_mesh_equations"],
            self.menu_parts["view_fit_best"],
            self.menu_parts["view_fit_default"],
            self.menu_parts["view_plots"],
            self.menu_parts["view_description"],
            self.menu_parts["view_annotation"],
            self.menu_parts["view_graph_circuit"]
        ])
        self.menu_parts["dropdown_component_menu"] = component_menu_dropdown
        self.menu_parts["dropdown_twoport"] = MenuDropdown('Twoport', 0, [
            self.menu_parts["create_twoport_a"],
            self.menu_parts["create_twoport_b"],
            self.menu_parts["create_twoport_g"],
            self.menu_parts["create_twoport_h"],
            self.menu_parts["create_twoport_s"],
            self.menu_parts["create_twoport_t"],
            self.menu_parts["create_twoport_y"],
            self.menu_parts["create_twoport_z"]
        ])
        self.menu_parts["dropdown_create_menu"] = MenuDropdown('Create', 1, [
            self.menu_parts["create_state_space"],
            self.menu_parts["create_transfer_function"],
            self.menu_parts["dropdown_twoport"]
        ])
        self.menu_parts["dropdown_inspect_menu"] = MenuDropdown('Inspect', 0, [
            self.menu_parts["inspect_voltage"],
            self.menu_parts["inspect_current"],
            self.menu_parts["inspect_thevenin_impedence"],
            self.menu_parts["inspect_norton_admittance"],
            self.menu_parts["inspect_noise_voltage"],
            self.menu_parts["inspect_noise_current"]
        ])
        self.menu_parts["dropdown_manipulate_menu"] = MenuDropdown('Manipulate', 0, [
            self.menu_parts["manipulate_independent_sources_kill"],
            self.menu_parts["manipulate_independent_sources_remove"],
            self.menu_parts["manipulate_model_ac"],
            self.menu_parts["manipulate_model_dc"],
            self.menu_parts["manipulate_model_transient"],
            self.menu_parts["manipulate_model_laplace"],
            self.menu_parts["manipulate_model_noise"],
            self.menu_parts["manupulate_expand_components"]
        ])
        self.menu_parts["dropdown_help_menu"] = MenuDropdown('Help', 0, [
            self.menu_parts["help"],
            self.menu_parts["launch_documentation"],
            self.menu_parts["help_debug"]
        ])

        menudropdowns = [self.menu_parts["dropdown_file_menu"], self.menu_parts["dropdown_edit_menu"], self.menu_parts["dropdown_view_menu"], self.menu_parts["dropdown_component_menu"], self.menu_parts["dropdown_create_menu"], self.menu_parts["dropdown_inspect_menu"], self.menu_parts["dropdown_manipulate_menu"], self.menu_parts["dropdown_help_menu"]]


        self.menubar = MenuBar(menudropdowns)
        self.menubar.make(self, self.level)

        self.popup_menu = None

        # Notebook tabs
        self.notebook = Notebook(self)

        self.canvases = []

        self.canvas = None

        if pathnames is None:
            pathnames = []

        for pathname in pathnames:
            try:
                self.load(pathname)
            except FileNotFoundError:
                self.new(pathname)

        if pathnames == []:
            model = self.new()

    def clear(self, grid='on'):

        self.canvas.drawing.clear(grid)

    def display(self):

        self.mainloop()

    def enter(self, canvas):

        self.canvas = canvas
        self.model = canvas.model
        self.sketcher = canvas.sketcher

        if self.debug:
            print(self.notebook.tab(self.notebook.select(), "text"))

    def load(self, pathname):
        model = self.new()

        if pathname is None:
            return

        model.load(pathname)
        self.set_filename(pathname)

    def set_filename(self, pathname):
        filename = basename(pathname)
        self.set_canvas_title(filename)

    def create_canvas(self, name, model):
        tab = Frame(self.notebook)

        canvas = Canvas(tab)
        canvas.pack(side=TOP, expand=True)

        self.notebook.add(tab, text=name)
        self.notebook.pack(fill=BOTH, expand=True)

        # Add the figure to the graph tab
        fig = Figure(figsize=self.FIGSIZE, frameon=False)
        fig.subplots_adjust(left=0, bottom=0, right=1,
                            top=1, wspace=0, hspace=0)

        graph = FigureCanvasTkAgg(fig, canvas)
        graph.draw()
        graph.get_tk_widget().pack(fill='both', expand=True)

        self.model = model
        drawing = Drawing(self, fig, self.debug)
        canvas.drawing = drawing
        canvas.tab = tab
        canvas.sketcher = Sketcher(canvas.drawing.ax, self.debug)

        tab.canvas = canvas

        self.canvases.append(canvas)

        # Display x, y position of cursor
        drawing.ax.format_coord = lambda x, y: "x:{0:.1f}, y:{1:.1f}".format(
            x, y)

        toolbar = NavigationToolbar2Tk(graph, canvas, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=BOTTOM, fill=X)

        self.notebook.select(len(self.canvases) - 1)

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_selected)

        canvas.model = model

        figure = canvas.drawing.fig
        canvas.bp_id = figure.canvas.mpl_connect('button_press_event',
                                                 self.on_click_event)

        canvas.br_id = figure.canvas.mpl_connect('button_release_event',
                                                 self.on_release_event)

        canvas.kp_id = figure.canvas.mpl_connect('key_press_event',
                                                 self.on_key_press_event)

        canvas.md_id = figure.canvas.mpl_connect('motion_notify_event',
                                                 self.on_mouse_event)
        canvas.ms_id = figure.canvas.mpl_connect('scroll_event',
                                                 self.on_mouse_scroll)

        canvas.rs_id = figure.canvas.mpl_connect('resize_event',
                                                 self.on_resize_event)

        canvas.sketcher.ax.callbacks.connect(
            'xlim_changed', self.on_mouse_zoom)

        canvas.sketcher.ax.callbacks.connect(
            'ylim_changed', self.on_mouse_zoom)

        self.enter(canvas)

        return canvas

    def new(self, name='untitled.sch'):

        model = self.uimodel_class(self)
        model.pathname = name
        canvas = self.create_canvas(name, model)
        self.model = model
        return model

    def on_ac_model(self, *args):
        self.model.on_ac_model()

    def on_add_con(self, thing):

        if self.debug:
            print('Adding connection ' + str(thing))

        self.model.on_add_con(thing)

    def on_add_cpt(self, thing):

        if self.debug:
            print('Adding component ' + str(thing))

        self.model.on_add_cpt(thing)

    def on_annotation(self, *args):
        # TODO: add args
        # TODO: need to support voltage and current labels
        cct = self.model.circuit.annotate_voltages(None)
        self.model.on_show_new_circuit(cct)

    def on_best_fit(self, *args):
        self.model.on_best_fit()

    def on_circuitgraph(self, *args):
        # TODO, save to png file and then display file
        self.model.circuit.cg.draw('/tmp/cg.png')
        self.show_image_dialog(
            '/tmp/cg.png', title='Circuit graph ' + self.model.pathname)

    def on_click_event(self, event):
        if event.xdata is None or event.ydata is None:
            # Can this happen?
            return
        if self.debug:
            print('Button event %s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))

        if event.dblclick:
            if event.button == 1:
                self.model.on_left_double_click(event.xdata, event.ydata)
            elif event.button == 3:
                self.model.on_right_double_click(event.xdata, event.ydata)
        else:
            if event.button == 1:
                self.model.on_left_click(event.xdata, event.ydata)
            elif event.button == 3:
                self.model.on_right_click(event.xdata, event.ydata)

    def on_release_event(self, event):

        if event.button == 1:
            self.model.on_mouse_release(event.key)

    def on_clone(self, *args):
        self.model.on_clone()

    def on_copy(self, *args):
        self.model.on_copy()

    def on_create_state_space(self, *args):
        self.model.on_create_state_space()

    def on_create_transfer_function(self, *args):
        self.model.on_create_transfer_function()

    def on_create_twoport(self, arg):
        kind = arg[0]
        self.model.on_create_twoport(kind)

    def on_cut(self, *args):
        self.model.on_cut()

    def on_dc_model(self, *args):
        self.model.on_dc_model()

    def on_debug(self, *args):
        self.model.on_debug()

    def on_default_fit(self, *args):
        self.canvas.drawing.set_default_view()
        self.refresh()

    def on_delete(self, *args):
        self.model.on_delete()

    def on_node_join(self, *args):
        self.model.on_node_join()
        self.model.on_redraw()

    def on_node_split(self, *args):
        print("Node Splitting not yet implemented")

    def on_description(self, *args):
        self.show_message_dialog(self.model.circuit.description())

    def report_callback_exception(self, exc, val, tb):
        # This catches exceptions but only for this window.
        # Each class needs to hook into this.
        from tkinter.messagebox import showerror

        if self.debug:
            breakpoint()

        showerror('Error', message=str(val))

    def on_enter(self, event):
        # TODO, determine tab from mouse x, y
        if self.debug:
            print('Enter %s, %s' % (event.x, event.y))

        self.enter(self.canvases[0])

    def on_exception(self, *args):
        from tkinter import messagebox
        import traceback

        if self.debug:
            breakpoint()

        err = traceback.format_exception(*args)
        messagebox.showerror('Exception', err)

    def on_expression(self, *args):
        self.model.on_expression()

    def on_edit_values(self, *args):
        self.show_edit_values_dialog()

    def on_expand(self, *args):
        self.model.on_expand()

    def on_export(self, *args):
        self.model.on_export()

    def on_help(self, *args):
        self.model.on_help()

    def launch_documentation(self, *args):
        import webbrowser

        webbrowser.open('https://lcapy-gui.readthedocs.io/')

    def on_inspect_properties(self, *args):
        self.model.on_inspect_properties()

    def on_inspect_current(self, *args):
        self.model.on_inspect_current()

    def on_inspect_noise_current(self, *args):
        self.model.on_inspect_noise_current()

    def on_inspect_noise_voltage(self, *args):
        self.model.on_inspect_noise_voltage()

    def on_inspect_norton_admittance(self, *args):
        self.model.on_inspect_norton_admittance()

    def on_inspect_thevenin_impedance(self, *args):
        self.model.on_inspect_thevenin_impedance()

    def on_inspect_voltage(self, *args):
        self.model.on_inspect_voltage()

    def on_key_press_event(self, event):
        key = event.key
        if self.debug:
            print(key)

        if key in self.model.key_bindings:
            self.model.key_bindings[key]()
        elif key in self.model.key_bindings_with_key:
            func, thing = self.model.key_bindings_with_key[key]
            func(thing)

    def on_key(self, event):
        key = event.char

        if self.debug:
            print('Key %s %s, %s, %s' % (key, event.keycode, event.x, event.y))
            print(event)

        if key in self.model.key_bindings_with_key:
            self.model.key_bindings_with_key[key](key)

    def on_key2(self, event, func):
        if self.debug:
            print('Key2', event, func)
        func()

    def on_laplace_model(self, *args):
        self.model.on_laplace_model()

    def on_library(self, *args):
        from lcapygui import __libdir__

        self.model.on_load(str(__libdir__))

    def on_load(self, *args):
        self.model.on_load()

    def on_manipulate_kill(self, *args):
        self.model.on_manipulate_kill()

    def on_manipulate_remove_sources(self, *args):
        self.model.on_manipulate_remove_sources()

    def on_mesh_equations(self, *args):
        self.model.on_mesh_equations()

    def on_modified_nodal_equations(self, *args):
        self.model.on_modified_nodal_equations()

    def on_mouse_event(self, event):

        if self.debug:
            if event.xdata is None or event.ydata is None:
                print('Mouse event: x=%d, y=%d, button=%d' %
                      (event.x, event.y, event.button))
            else:
                print('Mouse event: x=%d, y=%d, xdata=%f, ydata=%f' %
                      (event.x, event.y, event.xdata, event.ydata))

        if event.xdata is None or event.ydata is None:
            return
        else:
            # Save the mouse position
            self.model.mouse_position = (event.xdata, event.ydata)

        if event.button == 1:
            self.model.on_mouse_drag(event.xdata, event.ydata,
                                     event.key)



        if self.uimodel_class == UIModelDnD:
            self.model.on_mouse_move(event.xdata, event.ydata)

    def on_mouse_scroll(self, event):
        if self.debug:
            print("Mouse scroll event:")
            print(f"  x: {event.x}\n  y: {event.y}\n  direction: {event.button}")
        self.model.on_mouse_scroll(event.button, event.x, event.y)

    def on_mouse_zoom(self, ax):

        self.model.on_mouse_zoom(ax)

    def on_netlist(self, *args):
        self.model.on_netlist()

    def on_nodal_equations(self, *args):
        self.model.on_nodal_equations()

    def on_noise_model(self, *args):
        self.model.on_noise_model()

    def on_new(self, *args):
        self.model.on_new()

    def on_paste(self, *args):
        self.model.on_paste()

    def on_plots(self, *args):
        self.show_multiplot_dialog()

    def on_preferences(self, *args):
        self.model.on_preferences()

    def on_quit(self, *args):
        self.model.on_quit()

    def on_redo(self, *args):

        self.model.on_redo()

    def on_resize_event(self, event):

        self.model.on_resize()

    def on_save(self, *args):
        self.model.on_save()

    def on_save_as(self, *args):
        self.model.on_save_as()

    def on_screenshot(self, *args):
        self.model.on_screenshot()

    def on_simple_netlist(self, *args):
        self.model.on_simple_netlist()

    def on_tab_selected(self, event):
        notebook = event.widget
        tab_id = notebook.select()
        index = notebook.index(tab_id)

        # TODO: rethink if destroy a tab/canvas
        canvas = self.canvases[index]
        self.enter(canvas)

    def on_transient_model(self, *args):
        self.model.on_transient_model()

    def on_undo(self, *args):
        self.model.on_undo()

    def on_view(self, *args):
        self.model.on_view()

    def on_view_macros(self, *args):
        self.model.on_view_macros()

    def refresh(self):
        self.canvas.drawing.refresh()

    def quit(self):
        exit()

    def save(self, pathname):
        name = basename(pathname)
        self.set_canvas_title(name)

    def screenshot(self, pathname):
        self.canvas.drawing.savefig(pathname)

    def set_canvas_title(self, name):
        self.notebook.tab('current', text=name)

    def set_view(self, xmin, ymin, xmax, ymax):
        self.canvas.drawing.set_view(xmin, ymin, xmax, ymax)

    def show_approximate_dialog(self, expr, title=''):
        from .approximate_dialog import ApproximateDialog

        self.approximate_dialog = ApproximateDialog(expr, self, title)

    def show_edit_dialog(self, expr):
        from .edit_dialog import EditDialog

        self.edit_dialog = EditDialog(self, expr)

    def show_edit_values_dialog(self):
        from .edit_values_dialog import EditValuesDialog

        self.edit_values_dialog = EditValuesDialog(self)

    def show_equations_dialog(self, expr, title=''):
        from .equations_dialog import EquationsDialog

        self.equations_dialog = EquationsDialog(expr, self, title)

    def show_error_dialog(self, message):
        from tkinter.messagebox import showerror

        showerror('', message)

    def show_expr_dialog(self, expr, title=''):
        from .expr_dialog import ExprDialog

        self.expr_dialog = ExprDialog(expr, self, title)
        return self.expr_dialog

    def show_expr_attributes_dialog(self, expr, title=''):
        from .expr_attributes_dialog import ExprAttributesDialog

        self.expr_attributes_dialog = ExprAttributesDialog(expr, self, title)

    def show_help_dialog(self):
        from .help_dialog import HelpDialog

        self.help_dialog = HelpDialog()

    def show_image_dialog(self, filename, title=''):
        from .image_dialog import ImageDialog

        self.image_dialog = ImageDialog(self, filename, title)

    def show_inspect_dialog(self, cpt, title=''):
        from .inspect_dialog import InspectDialog

        self.inspect_dialog = InspectDialog(self, cpt, title)

    def inspect_properties_dialog(self, cpt, on_changed=None, title=''):
        from .cpt_properties_dialog import CptPropertiesDialog

        name = cpt.name
        if name in self.dialogs:
            self.dialogs[name].focus()
        else:
            dialog = CptPropertiesDialog(self, cpt, on_changed, title)
            self.dialogs[name] = dialog

    def show_info_dialog(self, message):
        from tkinter.messagebox import showinfo

        showinfo('', message)

    def show_limit_dialog(self, expr, title=''):
        from .limit_dialog import LimitDialog

        self.limit_dialog = LimitDialog(expr, self, title)

    def show_message_dialog(self, message, title=''):
        from .message_dialog import MessageDialog

        self.message_dialog = MessageDialog(message, title)

    def show_multiplot_dialog(self):
        from .multiplot_dialog import MultiplotDialog

        self.multiplot_dialog = MultiplotDialog(self)

    def show_node_properties_dialog(self, node, on_changed=None, title=''):
        from .node_properties_dialog import NodePropertiesDialog

        name = node.name
        if name in self.dialogs:
            self.dialogs[name].focus()
        else:
            dialog = NodePropertiesDialog(self, node, on_changed, title)
            self.dialogs[name] = dialog

    def show_plot_properties_dialog(self, expr):
        from .plot_properties_dialog import PlotPropertiesDialog

        self.plot_properties_dialog = PlotPropertiesDialog(expr, self)

    def show_preferences_dialog(self, on_changed=None):
        from .preferences_dialog import PreferencesDialog

        self.preferences_dialog = PreferencesDialog(self, on_changed)

    def show_first_launch_dialog(self):
        from .message_dialog import MessageDialog

        message = "Welcome to lcapy-gui.\nFor help on how to use this program, check out the documentation at https://lcapy-gui.readthedocs.io/"
        self.first_launch_dialog = MessageDialog(title="Welcome to Lcap-gui", message=message)

    def show_python_dialog(self, expr):
        from .python_dialog import PythonDialog

        self.python_dialog = PythonDialog(expr, self)

    def show_working_dialog(self, expr):
        from .working_dialog import WorkingDialog

        self.working_dialog = WorkingDialog(expr, self)
        return self.working_dialog

    def show_state_space_dialog(self, cpt):
        from .state_space_dialog import StateSpaceDialog

        self.state_space_dialog = StateSpaceDialog(self, cpt)

    def show_subs_dialog(self, expr, title=''):
        from .subs_dialog import SubsDialog

        self.subs_dialog = SubsDialog(expr, self, title)

    def show_transfer_function_dialog(self, cpt):
        from .transfer_function_dialog import TransferFunctionDialog

        self.transfer_function_dialog = TransferFunctionDialog(self, cpt)

    def show_twoport_dialog(self, cpt, kind):
        from .twoport_dialog import TwoportDialog

        self.twoport_dialog = TwoportDialog(self, cpt, kind)

    def show_twoport_select_dialog(self, TP, kind):
        from .twoport_select_dialog import TwoportSelectDialog

        self.twoport_select_dialog = TwoportSelectDialog(self, TP, kind)

    def show_warning_dialog(self, message):
        from tkinter.messagebox import showwarning

        showwarning('', message)

    def open_file_dialog(self, initialdir='.', doc='Lcapy netlist',
                         ext='*.sch'):

        from tkinter.filedialog import askopenfilename

        pathname = askopenfilename(initialdir=initialdir,
                                   title="Select file",
                                   filetypes=((doc, ext),))
        return pathname

    def save_file_dialog(self, pathname, doc='Lcapy netlist',
                         ext='*.sch'):

        from tkinter.filedialog import asksaveasfilename
        from os.path import dirname, splitext, basename

        dirname = dirname(pathname)
        filename = basename(pathname)
        basename, ext = splitext(filename)

        options = {}
        options['defaultextension'] = ext
        options['filetypes'] = ((doc, ext),)
        options['initialdir'] = dirname
        options['initialfile'] = basename
        options['title'] = "Save file"

        return asksaveasfilename(**options)

    def export_file_dialog(self, pathname, default_ext=None):
        from tkinter.filedialog import asksaveasfilename
        from os.path import dirname, splitext, basename

        dirname = dirname(pathname)
        basename, ext = splitext(basename(pathname))

        if default_ext is not None:
            ext = default_ext

        options = {}
        options['defaultextension'] = ext
        options['filetypes'] = (("Embeddable LaTeX", "*.schtex"),
                                ("Standalone LaTeX", "*.tex"),
                                ("PNG image", "*.png"),
                                ("SVG image", "*.svg"),
                                ("PDF", "*.pdf"))
        options['initialdir'] = dirname
        options['initialfile'] = basename + '.pdf'
        options['title'] = "Export file"

        return asksaveasfilename(**options)
