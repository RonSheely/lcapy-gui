from .components.sketch import Sketch


class SketchLibrary:

    def __init__(self):

        self.sketches = {}

    def _check_style(self, style):

        styles = ('american', 'british', 'european')
        if style not in styles:
            raise ValueError('Unsupported style %s, must be either %s'
                             % (style,  ', '.join(styles)))

    def lookup(self, sketch_key, style='american'):
        """
        Lookup a sketch by key and style.
        :param str sketch_key: The sketch to look up
        :param str style: The Component Style
        :return:
        :rtype: components.sketch.Sketch
        """
        self._check_style(style)

        if style not in self.sketches:
            self.sketches[style] = {}

        if sketch_key not in self.sketches[style]:

            sketch = Sketch.load(sketch_key, style=style, complain=True)
            self.sketches[style][sketch_key] = sketch

        return self.sketches[style][sketch_key]
