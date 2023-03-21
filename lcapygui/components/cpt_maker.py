from .admittance import Admittance
from .bjt import BJT
from .capacitor import Capacitor
from .cpe import CPE
from .current_source import CurrentSource
from .diode import Diode
from .ferritebead import FerriteBead
from .ground import Ground
from .impedance import Impedance
from .inductor import Inductor
from .jfet import JFET
from .mosfet import MOSFET
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

# Could use importlib.import_module to programmatically import
# the component classes.


class CptMaker:

    cpts = {
        'Ground': Ground,
        'C': Capacitor,
        'CPE': CPE,
        'D': Diode,
        'E': VCVS,
        'Opamp': Opamp,
        'F': CCCS,
        'FB': FerriteBead,
        'G': VCCS,
        'H': CCVS,
        'I': CurrentSource,
        'J': JFET,
        'L': Inductor,
        'M': MOSFET,
        'P': Port,
        'Q': BJT,
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

        if create:
            sketch = Sketch.create(cpt.sketch_key, cpt.sketch_net)

        sketch = Sketch.load(cpt.sketch_key)
        if sketch is None:
            raise FileNotFoundError(
                'Could not find data file for ' + cpt.sketch_key)
        return sketch

    def _make_cpt(self, cpt_type, kind='', style='', name=None,
                  nodes=None, opts=None):

        cls = self.cpts[cpt_type]

        try:
            cpt = cls(kind=kind, style=style,
                      name=name, nodes=nodes, opts=opts)
        except TypeError:
            cpt = cls(None, kind=kind, style=style, name=name,
                      nodes=None, opts=opts)

        return cpt

    def _add_sketch(self, cpt, create=False):

        sketch_key = cpt.sketch_key

        try:
            sketch = self.sketches[sketch_key]
        except KeyError:
            sketch = self._make_sketch(cpt, create)

        self.sketches[sketch_key] = sketch

        # TODO: remove duck typing
        cpt.sketch = sketch

    def __call__(self, cpt_type, kind='', style='', name=None,
                 nodes=None, opts=None, create=False):

        cpt = self._make_cpt(cpt_type, kind, style, name, nodes, opts)

        self._add_sketch(cpt, create)

        return cpt


cpt_maker = CptMaker()


def cpt_make(cpt_type, kind='', style='', name=None,
             nodes=None, opts=None, create=False):
    """Factory to create the sketch required to draw a component
    of `cpt_type`."""

    # There are two ways a cpt is made:
    # 1. From a specified pair of coordinates and a cpt type.
    # 2. When loading from a file where the nodes are known.

    return cpt_maker(cpt_type, kind, style, name, nodes, opts, create)


def cpt_remake(cpt):

    return cpt_maker._add_sketch(cpt)
