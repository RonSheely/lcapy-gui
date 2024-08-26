from xml.dom import minidom
from svgpathtools.parser import parse_transform
from svgpath2mpl import parse_path
from numpy import all

# TODO: look for style attribute, split by semicolon.  One of the most
# useful is fill, for example, 'fill:rgb(0%,0%,0%)' or 'fill:none'.
# The paths and use nodes have a style attribute.

# The SVG file has:
# 1. Symbol definitions
# 2. Clip paths
# 3. Drawing paths
# 4. Symbol uses
#
# It uses the <g> element to group other elements


def parse_style(string):

    style = {}
    parts = string.strip().split(';')
    for part in parts:
        bits = part.split(':')
        if len(bits) == 2:
            k, v = bits
            style[k] = v
    return style


class SVGPath:

    def __init__(self, path, transform, style, symbol):

        self.path = path
        self.transform = transform
        self.symbol = symbol
        self.style = style


class SVGParse:

    def __init__(self, filename):

        self.filename = filename

        doc = minidom.parse(filename)

        svg_paths = doc.getElementsByTagName('path')
        svg_defs = doc.getElementsByTagName('defs')
        svg_uses = doc.getElementsByTagName('use')

        svg = doc.getElementsByTagName('svg')[0]
        width_str = svg.getAttribute('width')
        height_str = svg.getAttribute('height')
        if not width_str.endswith('pt'):
            raise ValueError('Need to to handle other units.')
        if not height_str.endswith('pt'):
            raise ValueError('Need to to handle other units.')

        self.width = float(width_str[:-2])
        self.height = float(height_str[:-2])

        # Ignore paths for symbol defs and clip paths
        svg_paths = [path for path in svg_paths
                     if path.parentNode.tagName not in ('symbol', 'clipPath')]

        svg_ds = [path.getAttribute('d') for path in svg_paths]
        svg_styles = [path.getAttribute('style') for path in svg_paths]
        svg_transforms = [path.getAttribute('transform') for path in svg_paths]

        transforms = []
        for transform in svg_transforms:
            if transform == '':
                transform = 'matrix(1,0,0,1,0,0)'
            transforms.append(transform)
        svg_transforms = transforms

        self.paths = []
        for d, transform, style in zip(svg_ds, svg_transforms, svg_styles):
            path = parse_path(d)
            transform = parse_transform(transform)
            self.paths.append(
                SVGPath(path, transform, parse_style(style), False))

        if svg_defs != []:
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
                path = parse_path(symbols[symbol_id])
                transform = parse_transform(transform)
                self.paths.append(
                    SVGPath(path, transform, parse_style(style), True))
