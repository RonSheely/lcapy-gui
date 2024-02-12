from matplotlib.patches import PathPatch, Arc, Circle, Polygon
from matplotlib.path import Path
from math import degrees
from numpy import array


class Sketcher:

    def __init__(self, ax, debug=0):

        self.ax = ax
        self.debug = debug

    def clear(self):

        self.ax.clear()

    def remove(self, arg):

        if isinstance(arg, list):
            for patch in arg:
                self.ax.remove(patch)
        else:
            self.ax.remove(patch)

    def sketch(self, sketch, tf, **kwargs):

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

            path = path.transformed(tf)

            fill = kwargs.pop('fill', fill)

            if self.debug:
                color = ['red', 'yellow', 'orange',
                         'green', 'blue', 'violet'][m % 6]

            patch = PathPatch(path, fill=fill, color=color, **kwargs)
            patches.append(patch)
            self.ax.add_patch(patch)

        return patches

    def stroke_line(self, xstart, ystart, xend, yend, color='black', **kwargs):

        return self.ax.plot((xstart, xend), (ystart, yend),
                            color=color, **kwargs)

    def stroke_arc(self, x, y, r, theta1, theta2, **kwargs):

        r *= 2
        patch = Arc((x, y), r, r, 0, degrees(theta1),
                    degrees(theta2), **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_rect(self, xstart, ystart, width, height, **kwargs):
        # xstart, ystart top left corner

        xend = xstart + width
        yend = ystart + height

        lines = []
        lines.append(self.stroke_line(xstart, ystart, xstart, yend, **kwargs))
        lines.append(self.stroke_line(xstart, yend, xend, yend, **kwargs))
        lines.append(self.stroke_line(xend, yend, xend, ystart, **kwargs))
        lines.append(self.stroke_line(xend, ystart, xstart, ystart, **kwargs))
        return lines

    def stroke_filled_circle(self, x, y, radius=0.5, color='black',
                             alpha=0.5, **kwargs):

        patch = Circle((x, y), radius, fc=color, alpha=alpha, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_donut(self, x, y, radius=0.5, color='black',
                     alpha=0.5, **kwargs):
        """This is for drawing open nodes; the zorder is set so that
        they are drawn over wires."""

        patch1 = Circle((x, y), radius, fc='white', alpha=alpha, zorder=10,
                        **kwargs)
        patch2 = Circle((x, y), radius, fc=color, alpha=alpha, fill=False,
                        zorder=10, **kwargs)
        self.ax.add_patch(patch1)
        self.ax.add_patch(patch2)
        return [patch1, patch2]

    def stroke_circle(self, x, y, radius=0.5, color='black',
                      alpha=0.5, **kwargs):

        patch = Circle((x, y), radius, fill=False,
                       color=color, alpha=alpha, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_polygon(self, path, color='black', alpha=0.5,
                       fill=False, **kwargs):

        patch = Polygon(path, fc=color, alpha=alpha,
                        fill=fill, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_path(self, path, color='black', closed=False, **kwargs):

        lines = []
        for m in range(len(path) - 1):
            xstart, ystart = path[m]
            xend, yend = path[m + 1]

            lines.append(self.stroke_line(xstart, ystart,
                         xend, yend, color=color, **kwargs))
        if closed:
            xstart, ystart = path[0]
            lines.append(self.stroke_line(xstart, ystart,
                         xend, yend, color=color, **kwargs))
        return lines

    def text(self, x, y, text, ha='center', va='center', **kwargs):

        from lcapy.latex import latex_format_label

        # The matplotlib mathtext parser does not like
        # dollar signs inside mathrm, e.g., \mathrm{$A_2$}
        # text = r'$\mathrm{' + latex_format_label(text) + '}$'

        return self.ax.annotate(text, (x, y), ha=ha, va=va, **kwargs)
