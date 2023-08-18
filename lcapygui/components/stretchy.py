from .component import Component
from numpy import array, sqrt


class Stretchy(Component):

    can_stretch = True

    def draw(self, model, **kwargs):
        """
        Handles drawing specific features of components.
        """

        sketch = self._sketch_lookup(model)

        # Handle ports where nothing is drawn.
        if sketch is None:
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

        scale = float(self.scale)
        if scale > r:
            scale = r

        # Width in cm
        w = sketch.width / 72 * 2.54 * scale

        p1 = array((x1, y1))
        p2 = array((x2, y2))

        if r != 0:
            dw = array((dx, dy)) / r * (r - w) / 2
            p1p = p1 + dw
            p2p = p2 - dw
        else:
            # For zero length wires
            p1p = p1
            p2p = p2

        sketch.draw_old(model, offset=(p1p + p2p) / 2, angle=angle,
                        scale=scale, snap=True, **kwargs)

        # TODO: generalize
        kwargs.pop('mirror', False)
        kwargs.pop('invert', False)

        sketcher = model.ui.sketcher
        sketcher.stroke_line(*p1, *p1p, **kwargs)
        sketcher.stroke_line(*p2p, *p2, **kwargs)

        # For transistors.
        if len(self.nodes) == 3:

            x3, y3 = self.nodes[1].x, self.nodes[1].y

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dx = mx - x3
            dy = my - y3
            r = sqrt(dx**2 + dy**2)

            p3 = array((x3, y3))

            # Height in cm
            h = sketch.height / 72 * 2.54
            dh = array((dx, dy)) / r * (r - h)
            p3p = p3 + dh
            sketcher.stroke_line(*p3, *p3p, **kwargs)

        # TODO, add label, voltage_label, current_label, flow_label
