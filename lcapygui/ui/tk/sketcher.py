from matplotlib.patches import PathPatch, Arc, Circle, Polygon
from matplotlib.transforms import Affine2D
from matplotlib.path import Path
from math import degrees
from numpy import array


class Sketcher:

    def __init__(self, ax, debug=0):

        self.ax = ax
        self.debug = debug

    def stroke_line(self, xstart, ystart, xend, yend, color='black', **kwargs):

        return self.ax.plot((xstart, xend), (ystart, yend),
                            color=color, **kwargs)

    def stroke_arc(self, x, y, r, theta1, theta2, **kwargs):

        r *= 2
        patch = Arc((x, y), r, r, 0, degrees(theta1),
                    degrees(theta2), **kwargs)
        self.ax.add_patch(patch)
        return patch

    def clear(self):

        self.ax.clear()

    def stroke_rect(self, xstart, ystart, width, height, **kwargs):
        # xstart, ystart top left corner

        xend = xstart + width
        yend = ystart + height

        self.stroke_line(xstart, ystart, xstart, yend, **kwargs)
        self.stroke_line(xstart, yend, xend, yend, **kwargs)
        self.stroke_line(xend, yend, xend, ystart, **kwargs)
        self.stroke_line(xend, ystart, xstart, ystart, **kwargs)

    def stroke_filled_circle(self, x, y, radius=0.5, color='black',
                             alpha=0.5, **kwargs):

        patch = Circle((x, y), radius, fc=color, alpha=alpha, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_circle(self, x, y, radius=0.5, color='black',
                      alpha=0.5, **kwargs):

        patch = Circle((x, y), radius, fc='white',
                       color=color, alpha=alpha, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_polygon(self, path, color='black', alpha=0.5,
                       fill=False, **kwargs):

        patch = Polygon(path, fc=color, alpha=alpha,
                        fill=fill, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def text(self, x, y, text, **kwargs):

        from lcapy.latex import latex_format_label

        # The matplotlib mathtext parser does not like
        # dollar signs inside mathrm, e.g., \mathrm{$A_2$}
        # text = r'$\mathrm{' + latex_format_label(text) + '}$'

        return self.ax.annotate(text, (x, y), **kwargs)

    def stroke_path(self, path, color='black', **kwargs):

        for m in range(len(path) - 1):
            xstart, ystart = path[m]
            xend, yend = path[m + 1]

            self.stroke_line(xstart, ystart, xend, yend, color=color, **kwargs)

    def remove(self, patch):

        self.ax.remove(patch)

    def sketch(self, sketch, offset=(0, 0), scale=1, angle=0, **kwargs):

        kwargs = {**sketch.kwargs, **kwargs}

        gtransform = Affine2D().rotate_deg(angle).scale(scale * sketch.SCALE)
        gtransform = gtransform.translate(*offset)

        color = kwargs.pop('color', sketch.color)
        mirror = kwargs.pop('mirror', False)
        invert = kwargs.pop('invert', False)

        patches = []

        for m, spath in enumerate(sketch.paths):
            path = spath.path
            fill = spath.fill

            # Note, the SVG coordinate system has y going down the screen
            # but Matplotlib's coordinate system has y going up the screen.
            # Thus we need to invert the sense of mirror.

            if not mirror:
                vertices = path.vertices * (1, -1)
                path = Path(vertices, path.codes)
            if invert:
                vertices = path.vertices * (-1, 1)
                path = Path(vertices, path.codes)

            path = path.transformed(gtransform)

            if False and patches == []:
                print(path.vertices)

            fill = kwargs.pop('fill', fill)

            if self.debug:
                color = ['red', 'yellow', 'orange',
                         'green', 'blue', 'violet'][m % 6]

            patch = PathPatch(path, fill=fill, color=color, **kwargs)
            patches.append(patch)
            self.ax.add_patch(patch)

        return patches
