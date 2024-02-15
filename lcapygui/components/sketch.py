from lcapy import Circuit
from .tf import TF
from .svgparse import SVGParse
from os.path import join
from matplotlib.path import Path


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
    PT_TO_CM = 2.54 / 72
    # This is the node spacing used to create the sketch
    NODE_SPACING = 2

    def __init__(self, paths, width, height, **kwargs):

        self.paths = paths
        self.width = width
        self.height = height
        self.kwargs = kwargs

    @property
    def width_pt(self):

        return self.width

    @property
    def height_pt(self):

        return self.height

    @property
    def width_cm(self):

        return self.width_pt * self.PT_TO_CM

    @property
    def height_cm(self):

        return self.height_pt * self.PT_TO_CM

    @property
    def color(self):

        return self.kwargs.get('color', 'black')

    @classmethod
    def create(cls, sketch_key, sketch_net, style='american'):
        """This creates and stores a sketch file."""

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

    @classmethod
    def load(cls, sketch_key, style='american', complain=True):
        """This loads a sketch file give a sketch_key."""

        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg' / style
        svg_filename = dirname / (sketch_key + '.svg')

        if not svg_filename.exists():

            print('Could not find data file %s for %s' %
                  (svg_filename, sketch_key))
            import sys
            sys.exit()

            if complain:
                raise FileNotFoundError('Could not find data file %s for %s' %
                                        (svg_filename, sketch_key))
            return None

        sketch = cls.load_file(str(svg_filename))
        sketch = sketch.align(sketch_key)

        cpt_type, cpt_kind, cpt_style = sketch.parse_sketch_key(sketch_key)
        if cpt_type in ('J', 'M', 'Q'):
            sketch.width, sketch.height = sketch.height, sketch.width

        return sketch

    @classmethod
    def load_file(cls, svg_filename):
        """This loads a sketch file given a filename."""

        svg = SVGParse(svg_filename)

        sketch_paths = []
        for svga_path in svg.paths:
            sketch_path = SketchPath(
                svga_path.path, svga_path.style, svga_path.symbol)
            sketch_path = sketch_path.transform(TF(svga_path.transform))
            sketch_paths.append(sketch_path)

        sketch = cls(sketch_paths, svg.width, svg.height)
        return sketch

    def horizontal_wire_pair_offsets(self):

        candidates = []
        for path in self.paths:
            if len(path.path) >= 4 and all(path.path.codes[0:4] == (1, 2, 1, 2)):
                vertices = path.path.vertices
                if vertices[0][1] == vertices[1][1]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    candidates.append((xoffset, yoffset))

        if candidates == []:
            return None, None

        # Search for horizontal line with longest extent.
        xmin = 1000
        yoffset = 0
        for candidate in candidates:
            if candidate[0] < xmin:
                xmin = candidate[0]
                yoffset = candidate[1]

        return self.width / 2, yoffset

    def vertical_wire_pair_offsets(self):

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

        # Search for horizontal line with longest extent.
        ymin = 1000
        yoffset = 0
        for candidate in candidates:
            if candidate[1] < ymin:
                ymin = candidate[1]
                xoffset = candidate[0]

        return xoffset, self.height / 2

    def vertical_wire_offsets(self):

        # Look for vertical wire (for ground, sground, cground,
        # rground) Note, if look for horizontal wire first, get
        # incorrect offset for rground
        for path in self.paths:
            if len(path.path) == 2 and all(path.path.codes == (1, 2)):
                vertices = path.path.vertices
                if vertices[0][0] == vertices[1][0]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    return xoffset, yoffset

        return None, None

    def horizontal_wire_offsets(self):

        # Look for single horizontal wire (this is triggered by W components)
        for path in self.paths:
            if len(path.path) == 2 and all(path.path.codes == (1, 2)):
                vertices = path.path.vertices
                if vertices[0][1] == vertices[1][1]:
                    xoffset = vertices[0][0]
                    yoffset = vertices[0][1]
                    return self.width / 2, yoffset

        return None, None

    def parse_sketch_key(self, sketch_key):

        cpt_type = sketch_key
        cpt_kind = ''
        cpt_style = ''
        if '-' in cpt_type:
            parts = cpt_type.split('-')
            cpt_type = parts[0]
            cpt_kind = parts[1]
            if len(parts) == 3:
                cpt_style = parts[2]

        return cpt_type, cpt_kind, cpt_style

    def offsets(self, sketch_key):
        """Find the offsets required to centre the sketch.
        Currently transistors are not centered horizontally."""

        cpt_type, cpt_kind, cpt_style = self.parse_sketch_key(sketch_key)

        if cpt_type in ('fdopamp', ):
            xoffset, yoffset = self.width / 2 + 11, self.height / 2
        elif cpt_type in ('TF', ):
            xoffset, yoffset = self.width / 2, self.height / 2 + 1
        elif cpt_type in ('opamp', 'inamp'):
            xoffset, yoffset = self.width / 2, self.height / 2
        elif cpt_type in ('Q', ):
            # FIXME for M-pmos-pigfete
            # xoffset, yoffset1 = self.vertical_wire_pair_offsets()
            # xoffset1, yoffset = self.horizontal_wire_offsets()
            xoffset, yoffset = self.width / 2 + 2.8, self.height / 2
        elif cpt_type in ('M', ):
            xoffset, yoffset = self.width / 2 + 0.7, self.height / 2
        elif cpt_type in ('J', ):
            xoffset, yoffset = self.width / 2 + 0.5, self.height / 2
        elif cpt_type in ('C', 'CPE', 'D', 'E', 'F', 'G',
                          'H', 'I', 'L', 'R', 'SW', 'V', 'Y', 'Z'):
            xoffset, yoffset = self.horizontal_wire_pair_offsets()
        elif cpt_type in ('FB', 'W'):
            if cpt_style in ('vdd', 'vss', 'vcc', 'vee'):
                xoffset, yoffset = self.vertical_wire_offsets()
                yoffset = 0
            else:
                xoffset, yoffset = self.horizontal_wire_offsets()
                # Hack to simplify positioning
                xoffset = 0
        elif cpt_type in ('P', ):
            xoffset = 0
            yoffset = 0
        else:
            raise ValueError('No case for ' + sketch_key + ' in sketch.py')

        if xoffset is None or yoffset is None:
            print('Could not find offsets for ' + sketch_key)
            xoffset, yoffset = self.width / 2, self.height / 2

        return xoffset, yoffset

    def align(self, sketch_key):
        """Remove xoffset, yoffset from component."""

        xoffset, yoffset = self.offsets(sketch_key)

        if xoffset is None:
            return self

        paths = []
        for path in self.paths:
            paths.append(path.transform(TF().translate(-xoffset, -yoffset)))

        return self.__class__(paths, self.width, self.height, **self.kwargs)

    def draw(self, model, tf, **kwargs):

        sketcher = model.ui.sketcher

        # TODO, simplify  (tf.scale() but don't want to scale the offset)

        c = tf.transform((0, 0))

        tf = TF().rotate_deg(-tf.angle_deg).scale(tf.scale_factor *
                                                  self.PT_TO_CM / self.NODE_SPACING)
        tf = tf.translate(*c)

        return sketcher.sketch(self, tf, **kwargs)

    def minmax(self):

        xmin = 1000
        ymin = 1000
        xmax = -1000
        ymax = -1000
        for spath in self.paths:
            path = spath.path
            for v, c in zip(path.vertices, path.codes):
                if c in (Path.MOVETO, Path.LINETO):
                    pos = v
                    if pos[0] > xmax:
                        xmax = pos[0]
                    if pos[0] < xmin:
                        xmin = pos[0]
                    if pos[1] > ymax:
                        ymax = pos[1]
                    if pos[1] < ymin:
                        ymin = pos[1]

        return xmin, xmax, ymin, ymax
