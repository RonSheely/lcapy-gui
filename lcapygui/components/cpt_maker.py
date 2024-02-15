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
from .switch import Switch
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
        'SW': Switch,
        'TF': Transformer,
        'V': VoltageSource,
        'W': Wire,
        'Y': Admittance,
        'Z': Impedance
    }

    def __init__(self):

        self.sketches = {}

    def _make_gcpt(self, cpt_type, kind='', style='', name=None,
                  nodes=None, opts=None):

        if (cpt_type == 'W' or cpt_type == 'DW') and kind != '':
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

        gcpt = cls(kind=kind, style=style,
                  name=name, nodes=nodes, opts=opts)
        return gcpt

    def __call__(self, cpt_type, kind='', style='', name=None,
                 nodes=None, opts=None):

        gcpt = self._make_gcpt(cpt_type, kind, style, name, nodes, opts)

        return gcpt


cpt_maker = CptMaker()


def gcpt_make_from_cpt(cpt):
    # This is called when loading a schematic from a file.

    is_connection = False

    # Convert wire with implicit connection to a connection component.
    if cpt.type == 'W':
        for kind in Connection.kinds:
            # Note, the kind starts with a -.
            if kind[1:] in cpt.opts:
                is_connection = True
                break

    if not is_connection:
        kind = cpt._kind

    return cpt_maker(cpt.type, kind=kind, name=cpt.name,
                     nodes=cpt.nodes, opts=cpt.opts)


def gcpt_make_from_type(cpt_type, cpt_name='', kind='', style=''):

    return cpt_maker(cpt_type, name=cpt_name, kind=kind, style=style)


def gcpt_make_from_sketch_key(sketch_key):

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

    return gcpt_make_from_type(cpt_type, '', kind, style)
