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
                   LabelEntry('grid', 'Grid',
                              self.model.preferences.grid,
                              ('on', 'off'),
                              command=self.on_update),
                   LabelEntry('lw', 'Line width',
                              self.model.preferences.lw,
                              command=self.on_update),
                   LabelEntry('node_size', 'Node size',
                              self.model.preferences.node_size,
                              command=self.on_update)
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
        self.model.preferences.grid = self.labelentries.get('grid')
        self.model.preferences.lw = self.labelentries.get('lw')
        self.model.preferences.node_size = self.labelentries.get('node_size')

        if self.update:
            # Could check for changes
            self.update()

    def on_ok(self):

        self.on_update()

        self.master.destroy()

        self.model.preferences.save()
