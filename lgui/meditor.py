import sys
from matplotlib.pyplot import subplots, rcParams, show
import matplotlib.patches as patches
from matplotlib.backend_tools import ToolBase
from numpy import arange
from .components import Capacitor, CurrentSupply, Inductor, \
    Resistor, VoltageSupply, Wire
from math import sqrt, degrees, atan2


class Tool(ToolBase):

    def __init__(self, toolmanager, name, func):
        super(Tool, self).__init__(toolmanager, name)
        self.func = func

    def trigger(self, sender, event, data=None):
        self.func()


class AnalyzeTool(Tool):
    # default_keymap = 'ctrl+a'
    description = 'Analyze'


class EditTool(Tool):
    # default_keymap = 'ctrl+e'
    description = 'Edit'


class ExportTool(Tool):
    # default_keymap = 'ctrl+x'
    description = 'Export'


class LoadTool(Tool):
    # default_keymap = 'ctrl+l'
    description = 'Load'


class QuitTool(Tool):
    # default_keymap = 'q'
    description = 'Quit'


class SaveTool(Tool):
    # default_keymap = 'ctrl+s'
    description = 'Save'


class ViewTool(Tool):
    # default_keymap = 'ctrl+v'
    description = 'View'


class Nodes(list):

    def __init__(self):

        super(Nodes, self).__init__(self)

    def add(self, *nodes):

        for node in nodes:
            if node not in self:
                self.append(node)

    def clear(self):

        while self != []:
            self.pop()

    def debug(self):

        for node in self:
            print(node)

    def closest(self, x, y):

        for node in self:
            x1, y1 = node
            rsq = (x1 - x)**2 + (y1 - y)**2
            if rsq < 0.1:
                return node
        return None


class Components(list):

    def __init__(self):

        super(Components, self).__init__(self)
        self.kinds = {}

    def add(self, cpt):

        if cpt.TYPE not in self.kinds:
            self.kinds[cpt.TYPE] = 0
        self.kinds[cpt.TYPE] += 1
        # Hack, update component class to have this attribute
        cpt.cname = cpt.TYPE + '%d' % self.kinds[cpt.TYPE]
        self.append(cpt)

    def clear(self):

        while self != []:
            # TODO erase component
            self.pop()

    def debug(self):

        for cpt in self:
            print(cpt)

    def as_sch(self, step):

        nodes = {}

        node_count = 0

        elts = []
        for cpt in self:
            # Enumerate nodes (FIXME for node 0)
            for port in cpt.ports:
                if port.position not in nodes:
                    nodes[port.position] = node_count
                    node_count += 1

            parts = [cpt.cname]

            for port in cpt.ports:
                parts.append('%d' % nodes[port.position])

            if cpt.value is not None:
                parts.append(cpt.value)

            x1, y1 = cpt.ports[0].position
            x2, y2 = cpt.ports[1].position
            r = sqrt((x1 - x2)**2 + (y1 - y2)**2) / step

            if r == 1:
                size = ''
            else:
                size = '=%s' % r

            if y1 == y2:
                if x1 > x2:
                    attr = 'left' + size
                else:
                    attr = 'right' + size
            elif x1 == x2:
                if y1 > y2:
                    attr = 'down' + size
                else:
                    attr = 'up' + size
            else:
                angle = degrees(atan2(y2 - y1, x2 - x1))
                attr = 'rotate=%s' % angle
            parts.append('; ' + attr)

            elts.append(' '.join(parts))
        return '\n'.join(elts)

    def closest(self, x, y):

        for cpt in self:
            x1, y1 = cpt.ports[0].position
            x2, y2 = cpt.ports[1].position
            xmid = (x1 + x2) / 2
            ymid = (y1 + y2) / 2
            rsq = (xmid - x)**2 + (ymid - y)**2
            ssq = (x2 - x1)**2 + (y2 - y1)**2
            if rsq < 0.1 * ssq:
                return cpt
        return None


class Cursor:

    def __init__(self, ui, x, y):

        self.layer = ui.cursor_layer
        self.patch = None
        self.x = x
        self.y = y

    def draw(self, color='red'):

        self.patch = self.layer.stroke_filled_circle(self.x, self.y,
                                                     color, alpha=0.5)

    def remove(self):

        self.patch.remove()


class Cursors(list):

    def debug(self):

        for cursor in self:
            print('%s, %s' % (cursor.x, cursor.y))

    def remove(self):

        while self != []:
            cursor = self.pop()
            cursor.remove()


class Layer:

    def __init__(self, ax):

        self.ax = ax
        self.color = 'black'

    def stroke_line(self, xstart, ystart, xend, yend):

        return self.ax.plot((xstart, xend), (ystart, yend), '-',
                            color=self.color)

    def stroke_arc(self, x, y, r, theta1, theta2):

        patch = patches.Arc((x, y), r, r, 0, degrees(theta1), degrees(theta2))
        self.ax.add_patch(patch)
        return patch

    def clear(self):

        self.ax.clear()

    def stroke_rect(self, xstart, ystart, width, height):
        # xstart, ystart top left corner

        xend = xstart + width
        yend = ystart + height

        self.stroke_line(xstart, ystart, xstart, yend)
        self.stroke_line(xstart, yend, xend, yend)
        self.stroke_line(xend, yend, xend, ystart)
        self.stroke_line(xend, ystart, xstart, ystart)

    def stroke_filled_circle(self, x, y, color='black', alpha=0.5):

        patch = patches.Circle((x, y), 0.5, fc=color, alpha=alpha)
        self.ax.add_patch(patch)
        return patch

    def remove(self, patch):

        self.ax.remove(patch)


class History(list):

    def add(self, cptname, x1, y1, x2, y2):

        self.append('A %s %s %s %s %s' % (cptname, x1, y1, x2, y2))

    def add_node(self, x, y):

        self.append('N %s %s' % (x, y))

    def debug(self):

        for elt in self:
            print(elt)

    def load(self, filename):

        for _ in range(len(self)):
            self.pop()

        with open(filename, 'r') as fhandle:
            lines = fhandle.read_lines(self)

        for line in lines:
            self.append(line)

    def play(self, ui):

        for action in self:
            parts = action.split(' ')
            if parts[0] == 'A':
                ui.add(parts[1], float(parts[2]), float(parts[3]),
                       float(parts[4]))
            elif parts[0] == 'M':
                ui.move(float(parts[1]), float(parts[2]))
            elif parts[0] == 'R':
                ui.rotate(float(parts[1]))
            elif parts[0] == 'S':
                ui.select(parts[1])
            else:
                raise RuntimeError('Unknown command ' + action)

    def move(self, xshift, yshift):

        self.append('M %f %f' % (xshift, yshift))

    def rotate(self, angle):

        self.append('R %f' % angle)

    def save(self, filename):

        with open(filename, 'w') as fhandle:
            fhandle.write_lines(self)

    def select(self, cptname):

        self.append('S %s' % cptname)

    def unselect(self):

        self.append('U')


class ModelBase:

    STEP = 2
    SCALE = 0.25

    def __init__(self, ui):

        self.components = Components()
        self.nodes = Nodes()
        self.history = History()
        self.ui = ui
        self.edit_mode = True
        self.cct = None
        self.filename = ''

    # Drawing commands
    def add(self, cptname, x1, y1, x2, y2):

        # Create component from name
        if cptname == 'C':
            cpt = Capacitor(None)
        elif cptname == 'I':
            cpt = CurrentSupply(None)
        elif cptname == 'L':
            cpt = Inductor(None)
        elif cptname == 'R':
            cpt = Resistor(None)
        elif cptname == 'V':
            cpt = VoltageSupply(None)
        elif cptname == 'W':
            cpt = Wire()
        else:
            # TODO
            return

        cpt.ports[0].position = x1, y1
        cpt.ports[1].position = x2, y2

        self.components.add(cpt)
        self.nodes.add(cpt.ports[0].position, cpt.ports[0].position)

        cpt.__draw_on__(self, self.ui.component_layer)
        self.ui.refresh()

        self.select(cptname)

    def circuit(self):

        from lcapy import Circuit

        s = self.components.as_sch(self.STEP)
        # Note, need a newline so string treated as a netlist string
        s += '\n; draw_nodes=connections'
        cct = Circuit(s)
        return cct

    def analyze(self):

        self.cct = self.circuit()

    def draw(self, cpt, **kwargs):

        if cpt is None:
            return
        cpt.draw(**kwargs)

    def export(self, filename):

        cct = self.circuit()
        cct.draw(filename)

    def load(self, filename):

        from lcapy import Circuit

        self.filename = filename

        # TODO: FIXME
        # self.ui.component_layer.clear()
        self.components.clear()

        cct = Circuit(filename)
        sch = cct.sch

        # TODO: handle wails of protest if something wrong
        sch._positions_calculate()

        # TODO: centre nicely
        offsetx = 20
        offsety = 20

        elements = sch.elements
        for elt in elements.values():
            # TODO: allow component name and value
            self.add(elt.type, elt.nodes[0].pos.x + offsetx,
                     elt.nodes[0].pos.y + offsety,
                     elt.nodes[-1].pos.x + offsetx,
                     elt.nodes[-1].pos.y + offsety)

    def move(self, xshift, yshift):
        # TODO
        pass

    def rotate(self, angle):
        # TODO
        pass

    def save(self, filename):

        s = self.components.as_sch(self.STEP)

        with open(filename, 'w') as fhandle:
            fhandle.write(s)

    def select(self, cptname):
        pass

    def unselect(self):
        pass

    def view(self):

        cct = self.circuit()
        cct.draw()


class ModelMPH(ModelBase):

    def __init__(self, ui):

        super(ModelMPH, self).__init__(ui)

        self.cursors = Cursors()

    def draw_cursor(self, x, y):

        step = self.STEP
        x = (x + 0.5 * step) // step * step
        y = (y + 0.5 * step) // step * step

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

    def unselect(self):

        self.cursors.remove()
        self.ui.refresh()

    def on_add_node(self, x, y):

        self.draw_cursor(x, y)
        self.history.add_node(x, y)

    def on_add_cpt(self, cptname):

        if len(self.cursors) < 2:
            # TODO
            return
        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        self.history.add(cptname, x1, y1, x2, y2)
        self.add(cptname, x1, y1, x2, y2)

    def on_analyze(self):

        if self.edit_mode:
            self.edit_mode = False
            self.cursors.remove()
            self.ui.refresh()

        self.analyze()

    def on_close(self):

        self.quit()

    def on_debug(self):

        print('Netlist.........')
        print(self.components.as_sch(self.STEP))
        print('Cursors.........')
        self.cursors.debug()
        print('Components......')
        self.components.debug()
        print('Nodes...........')
        self.nodes.debug()
        print('History.........')
        self.history.debug()

    def on_edit(self):

        self.edit_mode = True

    def on_export(self):

        filename = self.ui.export_file_dialog(self.filename)
        if filename == '':
            return
        self.export(filename)

    def on_move(self, xshift, yshift):
        self.history.move(xshift, yshift)
        self.move(xshift, yshift)

    def on_rotate(self, angle):
        self.history.rotate(angle)
        self.rotate(angle)

    def on_select(self, cptname):
        self.select(cptname)

    def on_unselect(self):
        self.history.unselect()
        self.unselect()

    def on_key(self, key):

        if key == 'ctrl+c':
            self.ui.quit()
        elif key == 'ctrl+d':
            self.on_debug()
        elif key == 'ctrl+l':
            self.on_load()
        elif key == 'ctrl+s':
            self.on_save()
        elif key == 'ctrl+v':
            self.on_view()
        elif key == 'escape':
            self.on_unselect()
        elif key in ('c', 'i', 'l', 'r', 'v', 'w'):
            self.on_add_cpt(key.upper())

    def on_left_click(self, x, y):

        cpt = self.components.closest(x, y)
        node = self.nodes.closest(x, y)

        # TODO: in future want to be able to edit node attributes as
        # well as place cursor on node.  Perhaps have an inspect mode?
        # The easiest option is to use a different mouse button but
        # this not available in browser implementations.

        if node:
            print(node)

        if cpt and node:
            print('Selected both node %s and cpt %s' % (node, cpt))

        if cpt is None:
            if self.edit_mode:
                self.on_add_node(x, y)
        else:
            # TODO, select component
            print(cpt.cname)
            if not self.edit_mode:
                # Better to have a tooltip
                self.ui.show_message_dialog(str(self.cct[cpt.cname].v))

    def on_load(self):

        filename = self.ui.open_file_dialog()
        if filename == '':
            return
        self.load(filename)

    def on_right_click(self, x, y):

        pass

    def on_save(self):

        filename = self.ui.save_file_dialog(self.filename)
        if filename == '':
            return
        self.save(filename)

    def on_undo(self):
        command = self.history.pop()
        print(command)
        # TODO, undo...

    def on_view(self):

        self.view()


class EditorBase:
    pass


class MatplotlibEditor(EditorBase):

    FIG_WIDTH = 6
    FIG_HEIGHT = 4

    XSIZE = 60
    YSIZE = 40

    def __init__(self, filename=None):

        # Default Linux backend was TkAgg now QtAgg
        # Default Windows backend Qt4Agg
        import matplotlib.pyplot as p
        print(p.get_backend())
        # Need TkAgg if using Tkinter file dialogs
        p.switch_backend('TkAgg')

        super(MatplotlibEditor, self).__init__()
        self.model = ModelMPH(self)

        rcParams['keymap.xscale'].remove('L')
        rcParams['keymap.xscale'].remove('k')
        rcParams['keymap.yscale'].remove('l')
        rcParams['keymap.save'].remove('s')
        rcParams['keymap.save'].remove('ctrl+s')

        rcParams['toolbar'] = 'toolmanager'
        self.fig, self.ax = subplots(1, figsize=(self.FIG_WIDTH,
                                                 self.FIG_HEIGHT))
        self.fig.subplots_adjust(
            left=0.1, top=0.9, bottom=0.1, right=0.9)
        self.ax.axis('equal')

        # Tools to add to the toolbar
        tools = [
            ['Load', LoadTool, self.model.on_load],
            ['Save', SaveTool, self.model.on_save],
            ['Export', ExportTool, self.model.on_export],
            ['View', ViewTool, self.model.on_view],
            ['Edit', EditTool, self.model.on_edit],
            ['Analyze', AnalyzeTool, self.model.on_analyze],
            ['Quit', QuitTool, self.quit]]

        for tool in tools:
            self.fig.canvas.manager.toolmanager.add_tool(tool[0],
                                                         tool[1],
                                                         func=tool[2])
            self.fig.canvas.manager.toolbar.add_tool(tool[0], 'toolgroup')

        self.fig.canvas.mpl_connect('close_event', self.on_close)

        xticks = arange(self.XSIZE)
        yticks = arange(self.YSIZE)
        self.ax.set_xlim(0, self.XSIZE)
        self.ax.set_ylim(0, self.YSIZE)
        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid()

        # TODO: matplotlib uses on layer
        layer = Layer(self.ax)

        self.cursor_layer = layer
        self.active_layer = layer
        self.component_layer = layer
        self.grid_layer = layer

        # self.ax.spines['left'].set_color('none')
        # self.ax.spines['right'].set_color('none')
        # self.ax.spines['bottom'].set_color('none')
        # self.ax.spines['top'].set_color('none')

        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.on_click_event)

        self.kp_cid = self.fig.canvas.mpl_connect('key_press_event',
                                                  self.on_key_press_event)

        self.fig.canvas.mpl_connect('close_event', self.on_close)

        # Make fullscreen
        self.fig.canvas.manager.full_screen_toggle()

        # self.set_title()

        if filename is not None:
            self.model.load(filename)

    def display(self):

        show()

    def refresh(self):

        self.fig.canvas.draw()

    def on_key_press_event(self, event):

        # Might be in the textboxes...
        if event.inaxes != self.ax:
            return

        key = event.key
        self.model.on_key(key)

    def on_click_event(self, event):

        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

        if event.button == 1:
            self.model.on_left_click(event.xdata, event.ydata)
        elif event.button == 3:
            self.model.on_right_click(event.xdata, event.ydata)

    def on_close(self, event):

        self.model.on_close()

    def quit(self):

        sys.exit()

    def show_message_dialog(self, message):

        from tkinter.messagebox import showinfo
        showinfo('', message)

    def open_file_dialog(self, initialdir='.'):

        from tkinter.filedialog import askopenfilename

        filename = askopenfilename(initialdir=initialdir,
                                   title="Select file",
                                   filetypes=(("Lcapy netlist", "*.sch"),))
        return filename

    def save_file_dialog(self, filename):

        from tkinter.filedialog import asksaveasfilename
        from os.path import dirname, splitext, basename

        dirname = dirname(filename)
        basename, ext = splitext(basename(filename))

        options = {}
        options['defaultextension'] = ext
        options['filetypes'] = (("Lcapy netlist", "*.sch"),)
        options['initialdir'] = dirname
        options['initialfile'] = filename
        options['title'] = "Save file"

        return asksaveasfilename(**options)

    def export_file_dialog(self, filename):

        from tkinter.filedialog import asksaveasfilename
        from os.path import dirname, splitext, basename

        dirname = dirname(filename)
        basename, ext = splitext(basename(filename))

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