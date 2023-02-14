from matplotlib.path import Path
import matplotlib.patches as patches
from numpy import array, dot, sin, cos, radians
from ...components import Multiline, Circle, Arc


class Drawing(list):

    def add(self, patch):

        self.append(patch)

    def remove(self):

        for patch in self:
            patch.remove()


class PictureDrawer:

    def __init__(self, ax):

        self.ax = ax

    def R(self, scale, angle):

        theta = radians(angle)
        c = cos(theta)
        s = sin(theta)
        R = array(((c, -s), (s, c))) * scale
        return R

    def _draw_multiline(self, thing, offset=(0, 0), scale=1, angle=0,
                        **kwargs):

        offset = array(offset)

        R = self.R(scale, angle)

        verts = []
        codes = []

        for point in thing.points:
            tpoint = dot(R, point) + offset
            verts.append(tpoint)
            if codes == []:
                codes.append(Path.MOVETO)
            else:
                codes.append(Path.LINETO)
        path = Path(verts, codes)

        patch = patches.PathPatch(path, **kwargs)
        return patch

    def _draw_circle(self, thing, offset=(0, 0), scale=1, angle=0,
                     **kwargs):

        R = self.R(scale, angle)
        toffset = dot(R, thing.centre) + offset

        return patches.Circle(toffset, thing.radius * scale,
                              **kwargs)

    def _draw_arc(self, thing, offset=(0, 0), scale=1, angle=0,
                  **kwargs):

        R = self.R(scale, angle)
        toffset = dot(R, thing.centre) + offset
        radius = thing.radius * scale

        # Circular arc
        return patches.Arc(toffset, radius, radius, angle=0,
                           theta1=thing.theta1 + angle,
                           theta2=thing.theta2 + angle,
                           **kwargs)

    def draw(self, pic, offset=(0, 0), scale=1, angle=0, **kwargs):

        drawing = Drawing()
        for thing in pic.things:
            if isinstance(thing, Multiline):
                func = self._draw_multiline
            elif isinstance(thing, Circle):
                func = self._draw_circle
            elif isinstance(thing, Arc):
                func = self._draw_arc
            else:
                raise ValueError('Unhandled class ' + str(thing))

            ckwargs = {**thing.kwargs, **pic.kwargs, **kwargs}

            patch = func(thing, offset, scale, angle, **ckwargs)
            self.ax.add_patch(patch)
            drawing.add(patch)

        return drawing

    def remove(self, patches):

        for patch in patches():
            patch.remove()


def test():

    from ..components import Picture
    import matplotlib.pyplot as plt

    pic = Picture(Multiline((0, 0), (0, 2), (1, 2), (0, 4),
                            (-1, 2), (0, 2), fc='orange'),
                  Circle((0, 4.5), 0.5),
                  Arc((0, 0), 1, 0, 180))

    fig, ax = plt.subplots()
    drawer = PictureDrawer(ax)

    drawing = drawer.draw(pic, offset=(1, 1), scale=1,
                          angle=45, ec='black', lw=2)
    ax.axis('equal')
    ax.set_ylim(0, 6)

    plt.show()

    # drawing.remove()
