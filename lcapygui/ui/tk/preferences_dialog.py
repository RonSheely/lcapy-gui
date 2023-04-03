from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class PreferencesDialog:

    def __init__(self, ui, update):

        self.model = ui.model
        self.update = update

        self.master = Tk()
        self.master.title('Preferences')

        entries = [LabelEntry('label_nodes', 'Node labels',
                              self.model.preferences.label_nodes,
                              ('all', 'none', 'alpha', 'pins',
                               'primary'), command=self.on_update),
                   LabelEntry('draw_nodes', 'Nodes',
                              self.model.preferences.draw_nodes,
                              ('all', 'none', 'connections', 'primary'),
                              command=self.on_update),
                   LabelEntry('label_cpts', 'Component labels',
                              self.model.preferences.label_cpts,
                              ('none', 'name',  'value', 'name+value'),
                              command=self.on_update),
                   LabelEntry('style', 'Style',
                              self.model.preferences.style,
                              ('american', 'british', 'european'),
                              command=self.on_update),
                   LabelEntry('voltage_dir', 'Voltage dir',
                              self.model.preferences.voltage_dir,
                              ('RP', 'EF'),
                              command=self.on_update),
                   LabelEntry('grid', 'Grid',
                              self.model.preferences.grid,
                              ('on', 'off'),
                              command=self.on_update),
                   LabelEntry('lw', 'Line width',
                              self.model.preferences.lw,
                              command=self.on_update),
                   LabelEntry('node_size', 'Node size',
                              self.model.preferences.node_size,
                              command=self.on_update),
                   LabelEntry('show_units', 'Show units',
                              self.model.preferences.show_units,
                              ('true', 'false'),
                              command=self.on_update),
                   LabelEntry('xsize', 'Width',
                              self.model.preferences.xsize,
                              command=self.on_update),
                   LabelEntry('ysize', 'Height',
                              self.model.preferences.ysize,
                              command=self.on_update),
                   LabelEntry('snap_grid', 'Snap to grid',
                              self.model.preferences.snap_grid,
                              ('true', 'false'),
                              command=self.on_update),
                   ]

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_update(self, arg=None):

        self.model.preferences.label_nodes = self.labelentries.get(
            'label_nodes')
        self.model.preferences.draw_nodes = self.labelentries.get('draw_nodes')
        self.model.preferences.label_cpts = self.labelentries.get('label_cpts')
        self.model.preferences.style = self.labelentries.get('style')
        self.model.preferences.voltage_dir = self.labelentries.get(
            'voltage_dir')
        self.model.preferences.grid = self.labelentries.get('grid')
        self.model.preferences.lw = self.labelentries.get('lw')
        self.model.preferences.node_size = self.labelentries.get('node_size')
        self.model.preferences.show_units = self.labelentries.get('show_units')
        self.model.preferences.xsize = self.labelentries.get('xsize')
        self.model.preferences.ysize = self.labelentries.get('ysize')
        self.model.preferences.snap_grid = self.labelentries.get('snap_grid')

        # Do not set show_units; this needs fixing in Lcapy since
        # str(expr) includes the units and this causes problems...

        if self.update:
            # Could check for changes
            self.update()

    def on_ok(self):

        self.on_update()

        self.master.destroy()

        self.model.preferences.save()
