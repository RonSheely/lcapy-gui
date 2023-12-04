from .component import Component
from .picture import Picture
from .pos import Pos
from numpy import array, sqrt


class Stretchy(Component):

    can_stretch = True

    def draw(self, model, **kwargs):
        """
        Handles drawing specific features of components.
        """

        sketch = self._sketch_lookup(model)

        # Handle ports where nothing is drawn.
        if sketch is None or self.type == 'P':
            return

        kwargs = self.make_kwargs(model, **kwargs)

        if 'invisible' in kwargs or 'nodraw' in kwargs or 'ignore' in kwargs:
            return

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        dx = x2 - x1
        dy = y2 - y1

        r = self.length
        if r == 0:
            model.ui.show_warning_dialog(
                'Ignoring zero size component ' + self.name)
            return

        angle = self.angle

        # This scales the component size but not the distance between
        # the nodes (default 1)
        scale = float(self.scale)
        if scale > r:
            scale = r

        # Width in cm
        w = sketch.width_cm * scale

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

        sketcher = model.ui.sketcher
        self.picture = Picture()
        self.picture.add(sketch.draw_old(model, offset=((p1p + p2p) / 2).xy,
                                         angle=angle, scale=scale,
                                         **kwargs))

        # TODO: generalize
        kwargs.pop('mirror', False)
        kwargs.pop('invert', False)

        self.picture.add(sketcher.stroke_line(*p1.xy, *p1p.xy, **kwargs))
        self.picture.add(sketcher.stroke_line(*p2p.xy, *p2.xy, **kwargs))

        # For transistors
        if False and len(self.nodes) == 3:

            x3, y3 = self.nodes[1].x, self.nodes[1].y

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dx = mx - x3
            dy = my - y3
            r = sqrt(dx**2 + dy**2)

            p3 = array((x3, y3))

            h = sketch.height_cm
            dh = array((dx, dy)) / r * (r - h)
            p3p = p3 + dh

            self.picture.add(sketcher.stroke_line(*p3, *p3p, **kwargs))

        # TODO, add label, voltage_label, current_label, flow_label
