from .admittance import Admittance
from .bjt import BJT
from .capacitor import Capacitor
from .connection import Connection
from .cpe import CPE
from .current_source import CurrentSource
from .diode import Diode
from .ferritebead import FerriteBead
from .impedance import Impedance
from .inductor import Inductor
from .jfet import JFET
from .mosfet import MOSFET
from .opamp import Opamp
from .opencircuit import OpenCircuit
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
        'O': OpenCircuit,
        'P': Port,
        'Q': BJT,
        'R': Resistor,
        'NR': Resistor,         # Noise free resistor
        'V': VoltageSource,
        'W': Wire,
        'X': Connection,
        'Y': Admittance,
        'Z': Impedance
    }

    def __init__(self):

        self.sketches = {}

    def _make_cpt(self, cpt_type, kind='', style='', name=None,
                  nodes=None, opts=None):

        if cpt_type == 'W' and kind != '':
            cls = Connection
        elif cpt_type == 'E' and kind == 'opamp':
            cls = Opamp
        else:
            cls = self.cpts[cpt_type]

        cpt = cls(kind=kind, style=style,
                  name=name, nodes=nodes, opts=opts)
        return cpt

    def _add_sketch(self, cpt):

        sketch_key = cpt.sketch_key

        try:
            sketch = self.sketches[sketch_key]
        except KeyError:
            sketch = Sketch.load(cpt.sketch_key)
            if sketch is None:
                raise FileNotFoundError(
                    'Could not find data file for ' + cpt.sketch_key)
            self.sketches[sketch_key] = sketch

        # TODO: remove duck typing
        cpt.sketch = sketch

    def __call__(self, cpt_type, kind='', style='', name=None,
                 nodes=None, opts=None, add_sketch=True):

        cpt = self._make_cpt(cpt_type, kind, style, name, nodes, opts)

        if add_sketch:
            self._add_sketch(cpt)

        return cpt


cpt_maker = CptMaker()


def cpt_make_from_cpt(cpt):

    ctype = cpt.type

    # Convert wire with implicit connection to a connection component.
    if ctype == 'W':
        for kind in Connection.kinds:
            if kind[1:] in cpt.opts:
                ctype = 'X'
                break

    return cpt_maker(ctype, kind=cpt._kind, name=cpt.name,
                     nodes=cpt.nodes, opts=cpt.opts)


def cpt_make_from_type(cpt_type, cpt_name='', kind='', style='',
                       add_sketch=True):

    return cpt_maker(cpt_type, name=cpt_name, kind=kind, style=style,
                     add_sketch=add_sketch)


def cpt_remake(cpt):

    return cpt_maker._add_sketch(cpt)


def cpt_sketch_make(cpt):

    # Could make method of cpt.
    sketch = Sketch.create(cpt.sketch_key, cpt.sketch_net)
    return sketch
