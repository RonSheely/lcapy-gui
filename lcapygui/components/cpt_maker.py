from .admittance import Admittance
from .capacitor import Capacitor
from .current_source import CurrentSource
from .diode import Diode
from .ground import Ground
from .impedance import Impedance
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

from .sketch import Sketch


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
        'NR': Resistor,         # Noise free resistor
        'V': VoltageSource,
        'W': Wire,
        'Y': Admittance,
        'Z': Impedance
    }

    def __init__(self):

        self.sketches = {}

    def _make_sketch(self, cpt, create=False):

        sketch = Sketch.load(cpt.sketch_key, cpt.xoffset, cpt.yoffset)
        if sketch is None:
            if create:
                sketch = Sketch.create(cpt.sketch_key, cpt.sketch_net)
            else:
                raise FileNotFoundError(
                    'Could not find data file for ' + cpt.sketch_key)
        return sketch

    def _make_cpt(self, cpt_type, kind=''):

        cls = self.cpts[cpt_type]

        try:
            cpt = cls(kind=kind)
        except TypeError:
            cpt = cls(None, kind=kind)

        return cpt

    def _add_sketch(self, cpt, create=False):

        sketch_key = cpt.sketch_key

        try:
            sketch = self.sketches[sketch_key]
        except KeyError:
            sketch = self._make_sketch(cpt, create)

        self.sketches[sketch_key] = sketch

        # TODO: remove duck type
        cpt.sketch = sketch

    def __call__(self, cpt_type, kind='', create=False):

        cpt = self._make_cpt(cpt_type, kind)

        self._add_sketch(cpt, create)

        return cpt


cpt_maker = CptMaker()


def cpt_make(cpt_type, kind='', create=False):
    """Factory to create the path required to draw a component
    of `cpt_type`."""

    return cpt_maker(cpt_type, kind, create)


def cpt_remake(cpt):

    return cpt_maker._add_sketch(cpt)
