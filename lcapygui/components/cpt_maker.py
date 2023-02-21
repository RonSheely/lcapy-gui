from .capacitor import Capacitor
from .current_source import CurrentSource
from .diode import Diode
from .ground import Ground
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

from lcapy import Circuit
from .svgparse import SVGParse
from .cpt_sketch import CptSketch


class CptMaker:

    cpts = {
        'Ground': Ground,
        'C': Capacitor,
        'D': Diode,
        'E': VCVS,
        'Opamp': Opamp,
        'F': CCCS,
        'G': VCCS,
        'H': CCVS,
        'I': CurrentSource,
        'L': Inductor,
        'P': Port,
        'R': Resistor,
        'V': VoltageSource,
        'W': Wire
    }

    def __init__(self):

        self.sketches = {}

    def _make_sketch(self, cpt):
        from lcapygui import __datadir__

        dirname = __datadir__ / 'svg'

        svg_filename = dirname / (cpt.sketch_key + '.svg')

        if not svg_filename.exists():

            a = Circuit()

            net = cpt.sketch_net
            if net is None:
                return None
            if ';' not in net:
                net += '; right'

            a.add(net)

            a.draw(str(svg_filename), label_values=False, label_ids=False,
                   label_nodes=False, draw_nodes=False)

        svg = SVGParse(str(svg_filename))

        sketch = CptSketch(cpt, svg.paths, svg.transforms, svg.width,
                           svg.height)
        return sketch

    def _make_cpt(self, cpt_type, kind=''):

        cls = self.cpts[cpt_type]

        try:
            cpt = cls(kind=kind)
        except TypeError:
            cpt = cls(None, kind=kind)

        return cpt

    def __call__(self, cpt_type, kind=''):

        cpt = self._make_cpt(cpt_type, kind)

        sketch_key = cpt.sketch_key
        import pdb
        pdb.set_trace()

        try:
            sketch = self.sketches[sketch_key]
        except KeyError:
            sketch = self._make_sketch(cpt)

        self.sketches[sketch_key] = sketch

        # TODO: remove duck type
        cpt.sketch = sketch

        return cpt


cpt_maker = CptMaker()


def cpt_make(cpt_type, kind=''):
    """Factory to create the path required to draw a component
    of `cpt_type`."""

    return cpt_maker(cpt_type, kind)
