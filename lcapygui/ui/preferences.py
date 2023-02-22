from pathlib import Path
import json


class Preferences:

    def __init__(self):

        self.label_nodes = 'none'
        self.draw_nodes = 'connections'
        self.label_cpts = 'name'
        self.style = 'american'
        self.node_size = 0.15
        self.node_color = 'black'
        self.grid = 'on'
        self.lw = 1.2

    def _dirname(self):

        return Path('~/.lcapy/').expanduser()

    def load(self):

        dirname = self._dirname()
        if not dirname.exists():
            self.save()

    def save(self):

        dirname = self._dirname()
        if not dirname.exists():
            dirname.make()
        s = json.dumps(self, default=lambda o: o.__dict__,
                       sort_keys=True, indent=4)
        filename = dirname / 'preferences.json'
        filename.write_text(s)

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
