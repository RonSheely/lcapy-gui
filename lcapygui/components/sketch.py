from lcapy import Circuit
from matplotlib.transforms import Affine2D
from .svgparse import SVGParse
from os.path import join

from .tf import TF


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
    def load(cls, sketch_key, style='american', complain=True):

        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg' / style
        svg_filename = dirname / (sketch_key + '.svg')

        if not svg_filename.exists():

            if complain:
                raise FileNotFoundError('Could not find data file %s for %s' %
                                        (svg_filename, sketch_key))
            return None

        sketch = cls.load_file(str(svg_filename))
        sketch = sketch.align(sketch_key)
        return sketch

    @classmethod
    def load_file(cls, svg_filename):

        svg = SVGParse(svg_filename)

        sketch_paths = []
        for svga_path in svg.paths:
            sketch_path = SketchPath(
                svga_path.path, svga_path.style, svga_path.symbol)
            sketch_path = sketch_path.transform(Affine2D(svga_path.transform))
            sketch_paths.append(sketch_path)

        sketch = cls(sketch_paths, svg.width, svg.height)
        return sketch

    @classmethod
    def create(cls, sketch_key, sketch_net, style='american'):

        dirname = join('lcapygui', 'data', 'svg', style)
        svg_filename = join(dirname, sketch_key + '.svg')

        a = Circuit()

        net = sketch_net
        if net is None:
            return None
        if ';' not in net:
            net += '; right'

        a.add(net)

        a.draw(str(svg_filename), label_values=False, label_ids=False,
               label_nodes=False, draw_nodes=False, style=style)

    def transistor_offsets(self):

        xoffset = None
        yoffset = None

        # Look for pair of vertical wires
        candidates = []
        for path in self.paths:
            if len(path.path) >= 4 and all(path.path.codes[0:4] == (1, 2, 1, 2)):
                vertices = path.path.vertices
                if vertices[0][0] == vertices[1][0]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    candidates.append((xoffset, yoffset))

        if candidates == []:
            return None, None

        # Search for vertical line with longest extent.
        ymin = 1000
        xoffset = 0
        for candidate in candidates:
            if candidate[1] < ymin:
                ymin = candidate[1]
                xoffset = candidate[0]

        print(xoffset)
        return xoffset, 0

    def offsets1(self, sketch_key):

        if sketch_key in ('fdopamp', ):
            return self.width / 2 + 11, self.height / 2
        elif sketch_key.startswith('TF'):
            return self.width / 2, self.height / 2 + 1
        elif sketch_key in ('opamp', 'inamp'):
            return self.width / 2, self.height / 2
        elif sketch_key.startswith('M') or sketch_key.startswith('Q') or sketch_key.startswith('J'):
            return self.transistor_offsets()

        xoffset = None
        yoffset = None

        # Look for pair of horizontal wires
        candidates = []
        for path in self.paths:
            if len(path.path) >= 4 and all(path.path.codes[0:4] == (1, 2, 1, 2)):
                vertices = path.path.vertices
                if vertices[0][1] == vertices[1][1]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    candidates.append((xoffset, yoffset))

        if False and candidates != []:
            # Search for horizontal line with longest extent.
            xmin = 1000
            yoffset = 0
            for candidate in candidates:
                if candidate[0] < xmin:
                    xmin = candidate[0]
                    yoffset = candidate[1]

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

    def offsets(self, sketch_key):

        xoffset, yoffset = self.offsets1(sketch_key)
        return xoffset, yoffset

    def align(self, sketch_key):
        """Remove xoffset, yoffset from component."""

        xoffset, yoffset = self.offsets(sketch_key)

        if xoffset is None:
            return self

        paths = []
        for path in self.paths:
            paths.append(path.transform(
                Affine2D().translate(-xoffset, -yoffset)))

        return self.__class__(paths, self.width, self.height, **self.kwargs)

    def draw_old(self, model, offset=(0, 0), scale=1, angle=0, **kwargs):

        sketcher = model.ui.sketcher

        tf = TF().rotate_deg(angle).scale(scale * self.SCALE)
        tf = tf.translate(*offset)

        return sketcher.sketch(self, tf, **kwargs)

    def draw(self, model, tf, **kwargs):

        sketcher = model.ui.sketcher

        # TODO, simplify  (tf.scale() but don't want to scale the offset)

        c = tf.transform((0, 0))

        tf = TF().rotate_deg(-tf.angle_deg).scale(tf.scale_factor * self.SCALE / model.STEP)
        tf = tf.translate(*c)

        return sketcher.sketch(self, tf, **kwargs)
