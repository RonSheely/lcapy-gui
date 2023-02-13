from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from numpy import array, dot, sin, cos, radians


class Thing:

    def R(self, scale, angle):

        theta = radians(angle)

        R = array(((cos(theta), -sin(theta)), (sin(theta), cos(theta)))) \
            * scale
        return R


class Multiline(Thing):

    def __init__(self, start, *points, **kwargs):

        self.start = start
        self.points = points
        self.kwargs = kwargs

    def patch(self, offset=(0, 0), scale=1, angle=0):

        offset = array(offset)

        R = self.R(scale, angle)
        tstart = dot(R, self.start) + offset

        verts = [tstart]
        codes = [Path.MOVETO]

        for point in self.points:
            tpoint = dot(R, point) + offset
            verts.append(tpoint)
            codes.append(Path.LINETO)
        path = Path(verts, codes)

        patch = patches.PathPatch(path, **self.kwargs)
        return patch


class Circle(Thing):

    def __init__(self, centre, radius, **kwargs):

        self.centre = centre
        self.radius = radius
        self.kwargs = kwargs

    def patch(self, offset=(0, 0), scale=1, angle=0):

        R = self.R(scale, angle)
        tstart = dot(R, self.centre) + offset

        return patches.Circle(tstart, self.radius * scale, **self.kwargs)


class Arc(Thing):

    def __init__(self, centre, radius, theta1, theta2, **kwargs):

        self.centre = centre
        self.radius = radius
        self.theta1 = theta1
        self.theta2 = theta2
        self.kwargs = kwargs

    def patch(self, offset=(0, 0), scale=1, angle=0):

        R = self.R(scale, angle)
        tstart = dot(R, self.centre) + offset
        radius = self.radius * scale

        # Circular arc
        return patches.Arc(tstart, radius, radius,
                           angle=0, theta1=self.theta1 + angle,
                           theta2=self.theta2 + angle, **self.kwargs)


class Picture:

    def __init__(self, *things):

        self.things = things

    def patches(self, offset, scale, angle):

        if hasattr(self, '_patches'):
            return self._patches

        patches = []
        for thing in self.things:
            patches.append(thing.patch(offset, scale, angle))

        self._patches = patches
        return patches

    def draw(self, ax, offset=(0, 0), scale=1, angle=0):

        for patch in self.patches(offset, scale, angle):
            ax.add_patch(patch)

    def remove(self):

        for patch in self.patches():
            patch.remove()


pic = Picture(Multiline((0, 0), (0, 2), (1, 2), (0, 4),
                        (-1, 2), (0, 2), facecolor='orange',
                        lw=2),
              Circle((0, 4.5), 0.5),
              Arc((0, 0), 1, 0, 180, lw=2))


fig, ax = plt.subplots()
pic.draw(ax, offset=(1, 1), scale=1, angle=45)
ax.axis('equal')
ax.set_ylim(0, 6)

# pic.remove()

plt.show()
