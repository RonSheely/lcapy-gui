from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D


class CptSketch:

    # Convert points to cm.
    SCALE = 2.54 / 72

    def __init__(self, cpt, paths, width, height):

        self.xoffset = cpt.xoffset
        self.yoffset = cpt.yoffset
        self.paths = paths
        self.width = width
        self.height = height

    def draw(self, axes, offset=(0, 0), scale=1, angle=0, **kwargs):

        gtransform = Affine2D().rotate_deg(angle).scale(scale * self.SCALE)
        gtransform = gtransform.translate(*offset)

        xoffset = self.xoffset
        yoffset = self.yoffset - self.height / 2

        patches = []
        for spath in self.paths:
            path = spath.path
            transform = spath.transform
            fill = spath.fill

            path = path.transformed(Affine2D(transform))
            path = path.transformed(Affine2D().translate(xoffset, yoffset))
            path = path.transformed(gtransform)

            if False and patches == []:
                print(path.vertices)

            patch = PathPatch(path, fill=fill, color='black', **kwargs)
            patches.append(patch)
            axes.add_patch(patch)

        return patches
