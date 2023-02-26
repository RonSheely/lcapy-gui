from lcapy import Circuit
from matplotlib.transforms import Affine2D
from .svgparse import SVGParse
from os.path import join


class SketchPath:

    def __init__(self, path, style, symbol):

        self.path = path
        self.style = style
        self.symbol = symbol

    @property
    def fill(self):

        return self.symbol or ('fill' in self.style and self.style['fill'] != 'none')

    def transform(self, transform):

        path = self.path.transformed(transform)

        return self.__class__(path, self.style, self.symbol)


class Sketch:

    # Convert points to cm.
    SCALE = 2.54 / 72

    def __init__(self, paths, width, height, **kwargs):

        self.paths = paths
        self.width = width
        self.height = height
        self.kwargs = kwargs

    @property
    def color(self):

        return self.kwargs.get('color', 'black')

    @classmethod
    def load(cls, sketch_key):

        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg'
        svg_filename = dirname / (sketch_key + '.svg')

        if not svg_filename.exists():
            return None

        svg = SVGParse(str(svg_filename))

        sketch_paths = []
        for svga_path in svg.paths:
            sketch_path = SketchPath(
                svga_path.path, svga_path.style, svga_path.symbol)
            sketch_path = sketch_path.transform(Affine2D(svga_path.transform))
            sketch_paths.append(sketch_path)

        sketch = cls(sketch_paths, svg.width, svg.height).align()
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

    def offsets(self):

        xoffset = None
        yoffset = None

        # Look for pair of horizontal wires
        for path in self.paths:
            if len(path.path) == 4 and all(path.path.codes == (1, 2, 1, 2)):
                vertices = path.path.vertices
                if vertices[0][1] == vertices[1][1]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    return 0, yoffset

        # Look for vertical wire (for ground, sground, cground, rground)
        # Note, if look for horizontal wire first, get incorrect offset for rground
        for path in self.paths:
            if len(path.path) == 2 and all(path.path.codes == (1, 2)):
                vertices = path.path.vertices
                if vertices[0][0] == vertices[1][0]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    return xoffset, yoffset

        # Look for single horizontal wire (this is triggered by W components)
        for path in self.paths:
            if len(path.path) == 2 and all(path.path.codes == (1, 2)):
                vertices = path.path.vertices
                if vertices[0][1] == vertices[1][1]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    return 0, yoffset

        return self.width / 2, self.height / 2

    def align(self):
        """Remove yoffset from component."""

        xoffset, yoffset = self.offsets()

        if xoffset is None:
            return self

        paths = []
        for path in self.paths:
            paths.append(path.transform(
                Affine2D().translate(-xoffset, -yoffset)))

        return self.__class__(paths, self.width, self.height, **self.kwargs)
