from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
from lcapy import Circuit
from .svgparse import SVGParse
from os.path import join


class Sketch:

    # Convert points to cm.
    SCALE = 2.54 / 72

    def __init__(self, paths, width, height, xoffset=0, yoffset=0, **kwargs):

        self.paths = paths
        self.width = width
        self.height = height
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.kwargs = kwargs

    @property
    def color(self):

        return self.kwargs.get('color', 'black')

    # This should be in a UI class.
    def draw(self, axes, offset=(0, 0), scale=1, angle=0, **kwargs):

        kwargs = {**self.kwargs, **kwargs}

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

            patch = PathPatch(path, fill=fill, color=self.color, **kwargs)
            patches.append(patch)
            axes.add_patch(patch)

        return patches

    @classmethod
    def load(cls, sketch_key, xoffset=0, yoffset=0):

        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg'
        svg_filename = dirname / (sketch_key + '.svg')

        if not svg_filename.exists():
            return None

        svg = SVGParse(str(svg_filename))

        sketch = cls(svg.paths, svg.width, svg.height,
                     xoffset, yoffset)
        return sketch

    @classmethod
    def create(cls, sketch_key, sketch_net):

        dirname = join('lcapygui', 'data', 'svg')
        svg_filename = join(dirname, sketch_key + '.svg')

        a = Circuit()

        net = sketch_net
        if net is None:
            return None
        if ';' not in net:
            net += '; right'

        a.add(net)

        a.draw(str(svg_filename), label_values=False, label_ids=False,
               label_nodes=False, draw_nodes=False)
