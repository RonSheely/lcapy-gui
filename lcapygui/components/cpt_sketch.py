from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D


class CptSketch:

    # Convert points to cm.
    SCALE = 2.54 / 72

    def __init__(self, cpt_type, paths, transforms, height):

        self.cpt_type = cpt_type
        self.paths = paths
        self.transforms = transforms
        self.height = height

    def draw(self, axes, offset=(0, 0), scale=1, angle=0, **kwargs):

        gtransform = Affine2D().rotate_deg(angle).scale(scale * self.SCALE)
        gtransform = gtransform.translate(*offset)

        patches = []
        for path, transform in zip(self.paths, self.transforms):

            path = path.transformed(Affine2D(transform))
            path = path.transformed(Affine2D().translate(0, -self.height / 2))
            path = path.transformed(gtransform)

            patch = PathPatch(path, fill=False, color='black', **kwargs)
            patches.append(patch)
            axes.add_patch(patch)
        return patches
