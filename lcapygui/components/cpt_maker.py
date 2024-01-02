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
from .inamp import Inamp
from .fdopamp import FDOpamp
from .opencircuit import OpenCircuit
from .port import Port
from .resistor import Resistor
from .transformer import Transformer
from .voltage_source import VoltageSource
from .wire import Wire
from .vcvs import VCVS
from .vccs import VCCS
from .ccvs import CCVS
from .cccs import CCCS

# Could use importlib.import_module to programmatically import
# the component classes.


class CptMaker:

    cpts = {
        'C': Capacitor,
        'CPE': CPE,
        'D': Diode,
        'E': VCVS,
        'opamp': Opamp,
        'inamp': Inamp,
        'fdopamp': FDOpamp,
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
        'TF': Transformer,
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
        elif cpt_type == 'E' and kind == 'inamp':
            cls = Inamp
        elif cpt_type == 'E' and kind == 'fdopamp':
            cls = FDOpamp
        elif cpt_type in self.cpts:
            cls = self.cpts[cpt_type]
        else:
            raise ValueError('Unsupported component ' + cpt_type)

        cpt = cls(kind=kind, style=style,
                  name=name, nodes=nodes, opts=opts)
        return cpt

    def __call__(self, cpt_type, kind='', style='', name=None,
                 nodes=None, opts=None):

        cpt = self._make_cpt(cpt_type, kind, style, name, nodes, opts)

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


def cpt_make_from_type(cpt_type, cpt_name='', kind='', style=''):

    return cpt_maker(cpt_type, name=cpt_name, kind=kind, style=style)


def cpt_make_from_sketch_key(sketch_key):

    parts = sketch_key.split('-', 2)
    cpt_type = parts[0]
    if len(parts) == 1:
        kind = ''
        style = ''
    elif len(parts) == 2:
        kind = parts[1]
        style = ''
    else:
        kind = parts[1]
        style = parts[2]

    return cpt_make_from_type(cpt_type, '', kind, style)
