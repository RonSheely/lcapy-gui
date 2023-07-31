from .components.sketch import Sketch, SketchPath
from .components.svgparse import SVGParse
from matplotlib.transforms import Affine2D


class SketchLibrary:

    def __init__(self, style='american'):

        self._style = None
        self.sketches = {}
        # This is the current style.
        self.style = style

    @property
    def style(self):

        return self._style

    @style.setter
    def style(self, style):

        styles = ('american', 'british', 'european')
        if style not in styles:
            raise ValueError(
                'Unsupported style %s, must be either %s'
                % (style,  ', '.join(styles)))

        if self._style == style:
            return

        self._style = style

    def load(self, sketch_key, complain=True):

        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg' / self.style
        svg_filename = dirname / (sketch_key + '.svg')

        if not svg_filename.exists():

            if complain:
                raise FileNotFoundError(
                    'Could not find data file %s for %s' %
                    (svg_filename, sketch_key))

            return None

        svg = SVGParse(str(svg_filename))

        sketch_paths = []
        for svga_path in svg.paths:
            sketch_path = SketchPath(
                svga_path.path, svga_path.style, svga_path.symbol)
            sketch_path = sketch_path.transform(Affine2D(svga_path.transform))
            sketch_paths.append(sketch_path)

        sketch = Sketch(sketch_paths, svg.width, svg.height).align(sketch_key)
        return sketch

    def lookup(self, sketch_key):

        if self.style not in self.sketches:
            self.sketches[self.style] = {}

        if sketch_key not in self.sketches[self.style]:

            sketch = self.load(sketch_key, complain=True)
            self.sketches[self.style][sketch_key] = sketch

        return self.sketches[self.style][sketch_key]
