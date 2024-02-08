from tkinter import Button
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class PreferencesDialog(Window):

    def __init__(self, ui, update):

        super().__init__(ui, None, 'Preferences')

        self.model = ui.model
        self.update = update

        entries = [LabelEntry('label_nodes', 'Node labels',
                              self.model.preferences.label_nodes,
                              ('all', 'none', 'alpha', 'pins',
                               'primary'), command=self.on_update),
                   LabelEntry('draw_nodes', 'Nodes',
                              self.model.preferences.draw_nodes,
                              ('all', 'none', 'connections', 'primary'),
                              command=self.on_update),
                   LabelEntry('label_style', 'Component labels',
                              self.model.preferences.label_style,
                              ('none', 'name', 'value', 'name=value',
                               'stacked', 'split'),
                              command=self.on_update),
                   LabelEntry('style', 'Style',
                              self.model.preferences.style,
                              ('american', 'british', 'european'),
                              command=self.on_update),
                   LabelEntry('voltage_dir', 'Voltage dir',
                              self.model.preferences.voltage_dir,
                              ('RP', 'EF'),
                              command=self.on_update),
                   LabelEntry('current_sign_convention',
                              'Current sign convention',
                              self.model.preferences.current_sign_convention,
                              ('passive', 'active', 'hybrid'),
                              command=self.on_update),
                   LabelEntry('grid', 'Grid',
                              self.model.preferences.grid,
                              ('on', 'off'),
                              command=self.on_update),
                   LabelEntry('scale', 'Scale',
                              self.model.preferences.scale,
                              command=self.on_update),
                   LabelEntry('line_width', 'Line width (pt)',
                              self.model.preferences.line_width,
                              command=self.on_update),
                   LabelEntry('font_size', 'Font size (pt)',
                              self.model.preferences.font_size,
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
                   LabelEntry('line_width_scale', 'Line width scale',
                              self.model.preferences.line_width_scale,
                              command=self.on_update),
                   LabelEntry('cpt_size',
                              'Component size (cm)',
                              self.model.preferences.cpt_size,
                              command=self.on_update),
                   LabelEntry('grid_spacing',
                              'Grid spacing',
                              self.model.preferences.grid_spacing,
                              command=self.on_update),
                   LabelEntry('color_scheme',
                              'Colour scheme',
                              self.model.preferences.color_scheme,
                              ('default', 'pastel', 'greyscale', 'pitch'),
                              command=self.on_update),
                   ]

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row, column=0)

        button = Button(self, text="Reset", command=self.on_reset)
        button.grid(row=self.labelentries.row, column=1)

    def on_update(self, arg=None):

        self.model.preferences.label_nodes = self.labelentries.get(
            'label_nodes')
        self.model.preferences.draw_nodes = self.labelentries.get('draw_nodes')
        self.model.preferences.label_style = self.labelentries.get(
            'label_style')
        self.model.preferences.style = self.labelentries.get('style')
        self.model.preferences.voltage_dir = self.labelentries.get(
            'voltage_dir')
        self.model.preferences.grid = self.labelentries.get('grid')
        self.model.preferences.line_width = self.labelentries.get('line_width')
        self.model.preferences.font_size = self.labelentries.get('font_size')
        self.model.preferences.scale = self.labelentries.get('scale')
        self.model.preferences.node_size = self.labelentries.get('node_size')
        self.model.preferences.show_units = self.labelentries.get('show_units')
        self.model.preferences.xsize = self.labelentries.get('xsize')
        self.model.preferences.ysize = self.labelentries.get('ysize')
        self.model.preferences.snap_grid = self.labelentries.get('snap_grid')
        self.model.preferences.current_sign_convention = self.labelentries.get(
            'current_sign_convention')
        self.model.preferences.line_width_scale = self.labelentries.get(
            'line_width_scale')
        self.model.preferences.cpt_size = self.labelentries.get(
            'cpt_size')
        self.model.preferences.grid_spacing = self.labelentries.get(
            'grid_spacing')
        self.model.preferences.color_scheme = self.labelentries.get(
            'color_scheme')

        # Do not set show_units; this needs fixing in Lcapy since
        # str(expr) includes the units and this causes problems...

        if self.update:
            # Could check for changes
            self.update()

    def on_ok(self):

        self.on_update()

        self.model.preferences.save()

        self.on_close()

    def on_reset(self):

        self.model.preferences.reset()

        self.model.preferences.save()

        if self.update:
            # Could check for changes
            self.update()

        # Might be better to update all the values rather than closing
        self.on_close()
