from .component import Component
from numpy import array, sqrt, dot, degrees
from numpy.linalg import norm
from math import atan2


class Transistor(Component):

    can_stretch = True
    label_offset = 0.6
    has_value = False
    # extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    # Perhaps make a circle
    hw = 0.25
    hh = 0.25
    bbox_path = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    @property
    def pins(self):
        if (self.kind is not None
            and (self.kind.startswith('pigfet')
                 or self.kind.startswith('nigfet'))):
            xpins = [[self.npins2, self.inpins2], [self.ppins2, self.ippins2]]
        else:
            xpins = [[self.npins, self.inpins], [self.ppins, self.ippins]]
        if (self.kind in ('pnp', 'jpf', 'pmos', 'pmosd', 'pfetd', 'pfet',
                          'pfetd-bodydiode', 'pfet-bodydiode'
                          'pigfetd', 'pigfete', 'pigfetebulk')):
            pins = xpins[not self.mirror][self.invert]
        else:
            pins = xpins[self.mirror][self.invert]

        # FIXME to not use size.
        if False and (self.size != 1 or self.scale != 1):

            if 'g' in pins:
                # Apply hack to draw gate in correct place when
                # size is not 1.  Only required if pos != 0.5.
                pins = pins.copy()
                gpin = pins['g']
                y = ((1 - self.scale) / 2 +
                     gpin[2] * self.scale + (self.size - 1) / 2) / self.size
                pins['g'] = (gpin[0], gpin[1], y)
        return pins

    @property
    def node1(self):

        return self.nodes[0]

    @property
    def node2(self):

        return self.nodes[2]

    @property
    def sketch_net(self):

        # With up, drain is down.
        s = self.type + ' 1 2 3 ' + self.cpt_kind + '; right'
        if self.symbol_kind != '':
            s += ', kind=' + self.symbol_kind
        return s
