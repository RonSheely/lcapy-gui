import matplotlib.patches as patches
from math import degrees


class Layer:

    def __init__(self, ax):

        self.ax = ax

    def stroke_line(self, xstart, ystart, xend, yend, color='black', **kwargs):

        return self.ax.plot((xstart, xend), (ystart, yend), '-',
                            color=color, **kwargs)

    def stroke_arc(self, x, y, r, theta1, theta2, **kwargs):

        r *= 2
        patch = patches.Arc((x, y), r, r, 0, degrees(theta1),
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

        patch = patches.Circle((x, y), radius, fc=color, alpha=alpha,
                               **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_circle(self, x, y, radius=0.5, color='black',
                      alpha=0.5, **kwargs):

        patch = patches.Circle((x, y), radius, fc='white',
                               color=color, alpha=alpha, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def stroke_polygon(self, path, color='black', alpha=0.5,
                       fill=False, **kwargs):

        patch = patches.Polygon(path, fc=color, alpha=alpha,
                                fill=fill, **kwargs)
        self.ax.add_patch(patch)
        return patch

    def text(self, x, y, text, **kwargs):

        return self.ax.annotate(text, (x, y), **kwargs)

    def stroke_path(self, path, color='black', **kwargs):

        for m in range(len(path) - 1):
            xstart, ystart = path[m]
            xend, yend = path[m + 1]

            self.stroke_line(xstart, ystart, xend, yend, color=color, **kwargs)

    def remove(self, patch):

        self.ax.remove(patch)
