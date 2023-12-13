from pathlib import Path
import json
from warnings import warn

# Perhaps make a dict?


class Preferences:

    circuitikz_default_line_width = 1.0
    circuitikz_default_scale = 1.0
    circuitikz_default_cpt_size = 1.5

    def __init__(self):

        self.version = 6
        self.label_nodes = 'none'
        self.draw_nodes = 'connections'
        self.label_cpts = 'name'
        self.style = 'american'
        self.voltage_dir = 'RP'
        self.grid = 'on'
        self.line_width = self.circuitikz_default_line_width
        self.scale = self.circuitikz_default_scale
        self.show_units = 'false'
        self.xsize = 16
        self.ysize = 10
        self.snap_grid = 'true'
        # This is the scaling used to set the circuitikz line width
        self.line_width_scale = 1.01
        self.node_size = 0.07
        self.node_color = 'black'
        self.current_sign_convention = 'passive'
        self.font_size = 18
        self.cpt_size = self.circuitikz_default_cpt_size
        # This is used as the reference for component attributes in
        # a .sch file.  For example, R 1 2; right.
        self.node_spacing = 2
        self.grid_spacing = 2

    def apply(self):

        from lcapy.state import state
        state.current_sign_convention = self.current_sign_convention

    @property
    def _dirname(self):

        return Path('~/.lcapy/').expanduser()

    @property
    def _filename(self):

        return self._dirname / 'preferences.json'

    def load(self):

        dirname = self._dirname
        if not dirname.exists():
            return

        s = self._filename.read_text()
        d = json.loads(s)

        version = d.pop('version')

        for k, v in d.items():
            setattr(self, k, v)

        if hasattr(self, 'lw'):
            warn('lw is superseded by line_width')
            self.line_width = float(v) / self.line_width_scale
            delattr(self, 'lw')

        if (hasattr(self, 'line_width')
                and not isinstance(self.line_width, float)):
            if self.line_width.endswith('pt'):
                self.line_width = float(self.line_width[:-2])

        if not hasattr(self, 'scale'):
            self.scale = self.circuitikz_default_scale

        # Update the preferences file if the version changed
        if version != self.version:
            self.save()

    def reset(self):

        self.__init__()

    def save(self):

        dirname = self._dirname
        if not dirname.exists():
            dirname.mkdir()
        s = json.dumps(self, default=lambda o: o.__dict__,
                       sort_keys=True, indent=4)

        self._filename.write_text(s)

    def schematic_preferences(self):

        opts = ('draw_nodes', 'label_nodes', 'style', 'voltage_dir')

        foo = []
        for opt in opts:
            foo.append(opt + '=' + getattr(self, opt))
        s = ', '.join(foo)

        if self.line_width != self.circuitikz_default_line_width:
            s += ', line width=' + str(self.line_width)
        if self.scale != self.circuitikz_default_scale:
            s += ', scale=%.2f' % self.scale
        if self.cpt_size != self.circuitikz_default_cpt_size:
            s += ', cpt_size=%.2f' % self.cpt_size

        if self.label_cpts == 'name':
            s += ', label_ids=true'
            s += ', label_values=false'
        elif self.label_cpts == 'value':
            s += ', label_ids=false'
            s += ', label_values=true'
        elif self.label_cpts == 'value+name':
            s += ', label_ids=true'
            s += ', label_values=true'

        return s
