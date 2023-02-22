from .components.port import Port
from numpy import array


class Node:

    def __init__(self, x, y, name):

        self.x = float(x)
        self.y = float(y)
        self.name = name
        self.count = 0
        self.cpts = []

    @property
    def position(self):

        return array((self.x, self.y))

    @position.setter
    def position(self, pos):

        self.x = pos[0]
        self.y = pos[1]

    def __str__(self):

        # Note, need to have float type otherwise 0 becomes empty string.
        x = str(round(self.x, 2)).rstrip('0').rstrip('.')
        y = str(round(self.y, 2)).rstrip('0').rstrip('.')

        return '%s@(%s, %s)' % (self.name, x, y)

    @property
    def is_primary(self):

        name = self.name
        parts = name.split('_')
        return (name[0] != '_' and len(parts) <= 2) \
            and not (name[0].isdigit() and len(parts) != 1)

    @property
    def port(self):

        for cpt in self.cpts:
            if isinstance(cpt, Port):
                return True
        return False

    def debug(self):

        s = str(self) + ', count=%s' % self.count

        names = [cpt.name for cpt in self.cpts]

        s += ', cpts=[%s]' % ', '.join(names) + '\n'

        return s
