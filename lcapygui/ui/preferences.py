from pathlib import Path
import json


# Perhaps make a dict?
class Preferences:

    def __init__(self):

        self.version = 1
        self.label_nodes = 'none'
        self.draw_nodes = 'connections'
        self.label_cpts = 'name'
        self.style = 'american'
        self.node_size = 0.1
        self.node_color = 'black'
        self.grid = 'on'
        self.lw = 1.2

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

    def save(self):

        dirname = self._dirname
        if not dirname.exists():
            dirname.make()
        s = json.dumps(self, default=lambda o: o.__dict__,
                       sort_keys=True, indent=4)

        self._filename.write_text(s)

    def schematic_preferences(self):

        opts = ('draw_nodes', 'label_nodes', 'style')

        foo = []
        for opt in opts:
            foo.append(opt + '=' + getattr(self, opt))
        s = ', '.join(foo)

        if self.label_cpts == 'name':
            s += ', label_ids=true'
        elif self.label_cpts == 'value':
            s += ', label_values=true'
        elif self.label_cpts == 'value+name':
            s += ', label_ids=true'
            s += ', label_values=true'

        return s
