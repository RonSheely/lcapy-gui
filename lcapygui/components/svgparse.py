from xml.dom import minidom
from svgpathtools.parser import parse_transform
from svgpath2mpl import parse_path


class SVGParse:

    def __init__(self, filename):

        self.filename = filename

        doc = minidom.parse(filename)

        svg_paths = doc.getElementsByTagName('path')
        svg_defs = doc.getElementsByTagName('defs')
        svg_gs = doc.getElementsByTagName('g')
        svg_uses = doc.getElementsByTagName('use')

        # Ignore paths for symbol defs and clip paths
        svg_paths = [path for path in svg_paths
                     if path.parentNode.tagName not in ('symbol', 'clipPath')]

        svg_ds = [path.getAttribute('d') for path in svg_paths]
        svg_transforms = [path.getAttribute(
            'transform') for path in svg_paths]

        transforms = []
        for transform in svg_transforms:
            if transform == '':
                transform = 'matrix(1,0,0,1,0,0)'
            transforms.append(transform)
        svg_transforms = transforms

        svg_symbols = svg_defs[0].getElementsByTagName('symbol')
        symbols = {}
        for symbol in svg_symbols:
            symbol_id = symbol.getAttribute('id')
            path = symbol.getElementsByTagName('path')[0]
            d = path.getAttribute('d')
            symbols[symbol_id] = d

        for use in svg_uses:
            symbol_id = use.getAttribute('xlink:href')[1:]
            x = use.getAttribute('x')
            y = use.getAttribute('y')
            transform = 'matrix(1,0,0,1,%s,%s)' % (x, y)
            svg_transforms.append(transform)
            svg_ds.append(symbols[symbol_id])

        self.transforms = []
        for transform in svg_transforms:
            self.transforms.append(parse_transform(transform))

        self.paths = []
        for d in svg_ds:
            self.paths.append(parse_path(d))


s = SVGParse('foo.svg')
