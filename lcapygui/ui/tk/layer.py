from matplotlib.patches import PathPatch, Arc, Circle, Polygon
from matplotlib.transforms import Affine2D
from math import degrees


class Layer:

    def __init__(self, ax):

        self.ax = ax

    def stroke_line(self, xstart, ystart, xend, yend, color='black', **kwargs):

        return self.ax.plot((xstart, xend), (ystart, yend), '-',
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

        xoffset = sketch.xoffset
        yoffset = sketch.yoffset - sketch.height / 2

        patches = []
        for spath in sketch.paths:
            path = spath.path
            transform = spath.transform
            fill = spath.fill

            path = path.transformed(Affine2D(transform))
            path = path.transformed(Affine2D().translate(xoffset, yoffset))
            path = path.transformed(gtransform)

            if False and patches == []:
                print(path.vertices)

            patch = PathPatch(path, fill=fill, color=sketch.color, **kwargs)
            patches.append(patch)
            self.ax.add_patch(patch)

        return patches
