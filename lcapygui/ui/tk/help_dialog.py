from tkinter import Tk
from tkhtmlview import HTMLLabel


class HelpDialog:

    message = r"""

<h1>Editing</h1>

Click on the grid to place a red positive node then click elsewhere
to place a blue negative node.  Then enter c for a capacitor, i for
a current source, l for an inductor, r for a resistor, v for a voltage
source, etc.  Alternatively, use the Components menu.  The escape key
will remove both the positive and negative nodes.

The attributes of a component (name, value, etc.) can be edited by
right clicking on a component.  Note, voltage and current sources
default to DC.  Select kind as step for transient analysis or specify
the value as a time domain function.

The attributes of a node can be edited by right clicking on a
node.  This is useful for defining a ground node.

<h1>Analysis</h1>

Select a component and use Inspect (ctrl+i) to find the voltage across
a component or the current through a component.  Note the polarity is
defined by the red (plus) and blue (minus) highlighted nodes.

Note, voltage and current sources default to DC.  This can be changed
by right clicking on the source and selecting `DC`, `AC`, `step`, or
`arbitrary`.  With `arbitrary`, the value can be an arbitrary
time-domain expression, for example, `4 * H(t) + 2`, where `H(t)` is
the Heaviside step.

<h1>Documentation</h1>

For further information about Lcapy, see
 <a href="https://lcapy-gui.readthedocs.io"> https://lcapy-gui.readthedocs.io </a>
and  <a href="https://lcapy.readthedocs.io"> https://lcapy.readthedocs.io </a>
"""

    def __init__(self):

        master = Tk()
        master.title('Help!')
        html_label = HTMLLabel(master, html=self.message)
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()
