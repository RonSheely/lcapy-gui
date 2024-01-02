from .pos import Pos
from .stretchy import Stretchy
from numpy import array, sqrt, dot


class Transistor(Stretchy):

    can_stretch = True
    has_value = False
    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}
    label_offset_pos = (0.5, 0)
    anotation_offset_pos = None
    label_alignment = ('left', 'center')

    # Perhaps make a circle?
    hw = 0.2
    hh = 0.2
    bbox_path = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    @property
    def is_ptype(self):
        return self.kind.startswith('pnp') or self.kind.startswith('pmos') or self.kind.startswith('pjf')

    @property
    def is_ntype(self):
        return self.kind.startswith('npn') or self.kind.startswith('nmos') or self.kind.startswith('njf')

    @property
    def node1(self):

        return self.nodes[0] if self.is_ntype else self.nodes[2]

    @property
    def node2(self):

        return self.nodes[2] if self.is_ntype else self.nodes[0]

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

        # Transistors are stretchy but only for the d, e, s, c wires.

        dx = x2 - x1
        dy = y2 - y1

        r = sqrt(dx**2 + dy**2)

        # This scales the component size but not the distance between
        # the nodes (default 1)
        scale = float(self.scale)
        if scale > r:
            scale = r

        # Width in cm
        w = 2 * scale

        p1 = Pos(x1, y1)
        p2 = Pos(x2, y2)

        if r != 0:
            dw = Pos(dx, dy) / r * (r - w) / 2
            p1p = p1 + dw
            p2p = p2 - dw
        else:
            # For zero length wires
            p1p = p1
            p2p = p2

        tf = self.make_tf(p1p, p2p,
                          self.pos1, self.pos2)
        if 'g' in self.pins:
            pin = self.pins['g']
        else:
            pin = self.pins['b']

        gatepos = tf.transform(pin[1:])
        xg, yg = gatepos

        positions = array(((x1, y1),
                          (xg, yg),
                          (x2, y2)))
        return positions
