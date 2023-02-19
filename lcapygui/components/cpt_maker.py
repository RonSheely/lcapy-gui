from .capacitor import Capacitor
from .current_source import CurrentSource
from .diode import Diode
from .inductor import Inductor
from .opamp import Opamp
from .port import Port
from .resistor import Resistor
from .voltage_source import VoltageSource
from .wire import Wire

from .vcvs import VCVS
from .vccs import VCCS
from .ccvs import CCVS
from .cccs import CCCS

# from .ground import Ground
# from .rground import RGround
# from .sground import SGround

from lcapy import Circuit
from os.path import exists, expanduser, join
from os import mkdir
from .svgparse import SVGParse
from .cpt_sketch import CptSketch


class CptMaker:

    # TODO, move cpts into classes

    cpts = {
        'C': ('C 1 2', Capacitor),
        'D': ('D 1 2', Diode),
        'Dled': ('D 1 2; kind=led', Diode),
        'Dzener': ('D 1 2; kind=zener', Diode),
        'E': ('E 1 2 3 4', VCVS),
        'Eopamp': ('E 1 2 opamp 3 4', Opamp),
        'F': ('E 1 2 3 4', CCCS),
        'G': ('E 1 2 3 4', VCCS),
        'H': ('E 1 2 3 4', CCVS),
        'I': ('I 1 2', CurrentSource),
        'Iac': ('I 1 2 ac', CurrentSource),
        'Idc': ('I 1 2 dc', CurrentSource),
        'L': ('L 1 2', Inductor),
        'P': ('P 1 2', Port),
        'R': ('R 1 2', Resistor),
        'V': ('V 1 2', VoltageSource),
        'Vac': ('V 1 2 ac', VoltageSource),
        'Vdc': ('V 1 2 dc', VoltageSource),
        'W': ('W 1 2', Wire),
    }

    def __init__(self):

        self.sketches = {}

    def _make_sketch(self, cpt_type):

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

        sketch = CptSketch(cpt_type, svg.paths, svg.transforms, svg.height)
        return sketch

    def __call__(self, cpt_type):

        try:
            sketch = self.sketches[cpt_type]
        except KeyError:
            sketch = self._make_sketch(cpt_type)

        self.sketches[cpt_type] = sketch

        cls = self.cpts[cpt_type][1]

        # TODO: tidy
        try:
            cpt = cls()
        except TypeError:
            cpt = cls(None)

        # TODO: remove duck type
        cpt.sketch = sketch

        return cpt


cpt_maker = CptMaker()


def cpt_make(cpt_type, kind=''):
    """Factory to create the path required to draw a component
    of `cpt_type`."""

    return cpt_maker(cpt_type)
