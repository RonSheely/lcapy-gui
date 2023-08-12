from pathlib import Path
import json
from warnings import warn

circuitikz_default_line_width = '0.4pt'
circuitikz_default_scale = 1.0

# Perhaps make a dict?


class Preferences:

    def __init__(self):

        self.version = 3
        self.label_nodes = 'none'
        self.draw_nodes = 'connections'
        self.label_cpts = 'name'
        self.style = 'american'
        self.node_size = 0.1
        self.node_color = 'black'
        self.grid = 'on'
        self.line_width = circuitikz_default_line_width,
        self.scale = circuitikz_default_scale
        self.show_units = 'false'
        self.xsize = 36
        self.ysize = 22
        self.snap_grid = 'true'
        self.voltage_dir = 'RP'
        # This is the scaling used to set the matplotlib lw argument
        self.line_width_scale = 3.5

        self.load()

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
        for k, v in d.items():
            setattr(self, k, v)

        if hasattr(self, 'lw'):
            warn('lw is superseded by line_width')
            self.line_width = str(float(v) / self.line_width_scale) + 'pt'
            delattr(self, 'lw')

        if not hasattr(self, 'scale'):
            self.scale = circuitikz_default_scale

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

        if self.line_width != circuitikz_default_line_width:
            s += ', line width=' + self.line_width
        if self.scale != circuitikz_default_scale:
            s += ', scale=%.2f' % self.scale

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
