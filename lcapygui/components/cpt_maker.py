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


class Bipole(CptSketch):

    can_stretch = True


class Capacitor(Bipole):
    pass


class CurrentSource(Bipole):
    pass


class Diode(Bipole):
    pass


class Inductor(Bipole):
    pass


class Opamp(CptSketch):
    pass


class Resistor(Bipole):
    pass


class VCVS(Bipole):
    pass


class VoltageSource(Bipole):
    pass


class CptMaker:

    # TODO, move cpts into classes

    cpts = {
        'C': ('C 1 2', Capacitor),
        'D': ('D 1 2', Diode),
        'Dled': ('D 1 2; kind=led', Diode),
        'Dzener': ('D 1 2; kind=zener', Diode),
        'E': ('E 1 2 3 4', VCVS),
        'Eopamp': ('E 1 2 opamp 3 4', Opamp),
        'I': ('I 1 2', CurrentSource),
        'Iac': ('I 1 2 ac', CurrentSource),
        'Idc': ('I 1 2 dc', CurrentSource),
        'L': ('L 1 2', Inductor),
        'R': ('R 1 2', Resistor),
        'V': ('V 1 2', VoltageSource),
        'Vac': ('V 1 2 ac', VoltageSource),
        'Vdc': ('V 1 2 dc', VoltageSource),
    }

    def __init__(self):

        self.sketches = {}

    def __call__(self, cpt_type):

        cls = self.cpts[cpt_type][1]

        try:
            return self.sketches[cpt_type]
        except KeyError:
            pass

        net = self.cpts[cpt_type][0]

        dirname = join(expanduser('~'), '.lcapygui')
        if not exists(dirname):
            mkdir(dirname)

        dirname = join(dirname, 'svg')
        if not exists(dirname):
            mkdir(dirname)

        svg_filename = join(dirname, cpt_type + '.svg')

        if not exists(svg_filename):

            a = Circuit()

            net = self.cpts[cpt_type][0]
            if ';' not in net:
                net += '; right'

            a.add(net)

            a.draw(svg_filename, label_values=False, label_ids=False,
                   label_nodes=False, draw_nodes=False)

        svg = SVGParse(svg_filename)
        paths = svg.paths
        transforms = svg.transforms

        sketch = cls(cpt_type, paths, transforms)
        self.sketches[cpt_type] = sketch
        return sketchc


cpt_maker = CptMaker()


def cpt_make(cpt_type):
    """Factory to create the path required to draw a component
    of `cpt_typ`."""

    return cpt_maker(cpt_type)
