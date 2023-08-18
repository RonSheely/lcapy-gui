from .stretchy import Stretchy
from numpy import array, sqrt, dot


class Transistor(Stretchy):

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

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions.

        x1, y1 defines the positive input node
        x2, y2 defines the negative input node"""

        dx = x1 - x2
        dy = y1 - y2
        r = sqrt(dx**2 + dy**2)
        R = array(((dx, -dy), (dy, dx))) / r

        # Midpoint
        ym = (y1 + y2) / 2
        xm = (x1 + x2) / 2

        # TODO: The offset might change with transistor types.
        # Note, the transistor base/gate is down.
        xg, yg = dot(R, (0, 2))
        xg += xm
        yg += ym

        # D G S
        positions = array(((x1, y1),
                           (xg, yg),
                           (x2, y2)))
        return positions
