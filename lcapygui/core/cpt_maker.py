from ..components.admittance import Admittance
from ..components.bjt import BJT
from ..components.capacitor import Capacitor
from ..components.connection import Connection
from ..components.cpe import CPE
from ..components.currentsource import CurrentSource
from ..components.damper import Damper
from ..components.diode import Diode
from ..components.ferritebead import FerriteBead
from ..components.impedance import Impedance
from ..components.inductor import Inductor
from ..components.jfet import JFET
from ..components.mass import Mass
from ..components.mosfet import MOSFET
from ..components.opamp import Opamp
from ..components.inamp import Inamp
from ..components.fdopamp import FDOpamp
from ..components.opencircuit import OpenCircuit
from ..components.port import Port
from ..components.resistor import Resistor
from ..components.spring import Spring
from ..components.switch import Switch
from ..components.transformer import Transformer
from ..components.voltagesource import VoltageSource
from ..components.wire import Wire
from ..components.vcvs import VCVS
from ..components.vccs import VCCS
from ..components.ccvs import CCVS
from ..components.cccs import CCCS
from ..components.dac import DAC
from ..components.adc import ADC

# Could use importlib.import_module to programmatically import
# the component classes.

# Perhaps iterate over kinds for each component class and
# index by cpt-type and cpt-kind?

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
        'k': Spring,
        'L': Inductor,
        'M': MOSFET,
        'm': Mass,
        'O': OpenCircuit,
        'P': Port,
        'Q': BJT,
        'R': Resistor,
        'r': Damper,
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
        elif cpt_type == 'U' and kind == 'adc':
            cls = ADC
        elif cpt_type == 'U' and kind == 'dac':
            cls = DAC
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
    # This is used when loading a schematic from a file.

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
    # This used when creating a new cpt from menu

    return cpt_maker(cpt_type, name=cpt_name, kind=kind, style=style)


def gcpt_make_from_sketch_key(sketch_key):
    # This is used only by sketchview

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
