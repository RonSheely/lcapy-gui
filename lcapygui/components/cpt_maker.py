from lcapy import Circuit
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
from os.path import exists, expanduser, join
from os import mkdir
from .svgparse import SVGParse


class CptSketch:

    def __init__(self, cpt_type, paths, transforms):

        self.cpt_type = cpt_type
        self.paths = paths
        self.transforms = transforms

    def draw(self, axes, offset=(0, 0), scale=1, angle=0, **kwargs):

        gtransform = Affine2D().rotate_deg(angle).scale(scale)
        gtransform = gtransform.translate(*offset)

        patches = []
        for path, transform in zip(self.paths, self.transforms):

            path = path.transformed(Affine2D(transform))
            path = path.transformed(gtransform)

            patch = PathPatch(path, fc='white', **kwargs)
            patches.append(patch)
            axes.add_patch(patch)
        return patches


class CptMaker:

    nets = {
        'R': ('R 1 2'),
        'C': ('C 1 2'),
        'L': ('L 1 2'),
        'V': ('V 1 2'),
        'Vac': ('V 1 2 ac'),
        'Vdc': ('V 1 2 dc'),
        'I': ('I 1 2'),
        'Iac': ('I 1 2 ac'),
        'Idc': ('I 1 2 dc'),
        'D': ('D 1 2'),
        'Dled': ('D 1 2; kind=led'),
        'Dzener': ('D 1 2; kind=zener'),
    }

    def __init__(self):

        self.sketches = {}

    def __call__(self, cpt_type):

        try:
            return CptSketch(cpt_type, self.sketches[cpt_type])
        except KeyError:
            pass

        net = self.nets[cpt_type]

        dirname = join(expanduser('~'), '.lcapygui')
        if not exists(dirname):
            mkdir(dirname)

        dirname = join(dirname, 'svg')
        if not exists(dirname):
            mkdir(dirname)

        svg_filename = join(dirname, cpt_type + '.svg')

        if not exists(svg_filename):

            a = Circuit()

            net = self.nets[cpt_type]
            if ';' not in net:
                net += '; right'

            a.add(net)

            a.draw(svg_filename, label_values=False, label_ids=False,
                   label_nodes=False, draw_nodes=False)

        svg = SVGParse(svg_filename)
        paths = svg.paths
        transforms = svg.transforms

        sketch = CptSketch(cpt_type, paths, transforms)
        self.sketches[cpt_type] = sketch
        return sketch


cpt_maker = CptMaker()


def cpt_make(cpt_type):
    """Factory to create the path required to draw a component
    of `cpt_typ`."""

    return cpt_maker(cpt_type)
