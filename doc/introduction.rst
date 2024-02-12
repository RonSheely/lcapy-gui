============
Introduction
============

Lcapy-tk allows a circuit schematic to be quickly created.  By
selecting a component, the potential difference across the component
or the current through the component can be displayed symbolically.

The schematic can be exported in a fancier form, as a PNG, PDF, SVG or
image.  Alternatively, the schematic can be converted to Circuitikz
macros.


Editing
=======

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


Analysis
========

Select a component and use Inspect (ctrl+i) to find the voltage across
a component or the current through a component.  Note the polarity is
defined by the red (plus) and blue (minus) highlighted nodes.

Note, voltage and current sources default to DC.  This can be changed
by right clicking on the source and selecting `DC`, `AC`, `step`, or
`arbitrary`.  With `arbitrary`, the value can be an arbitrary
time-domain expression, for example, `4 * H(t) + 2`, where `H(t)` is
the Heaviside step.


Preferences
===========

The preferences dialog controls the drawing style.


Schematics
==========

Schematics can be exported in a number of formats.  Circuitikz is used
to generate text-book quality schematics.  The format is determined by
the file extension:

- pgf Portable Graphics Format (this can be input into a LaTeX document)

- tex This is a standalone TeX file

- svg Scalar Vector Graphics

- pdf Portable Document Format

- png Portable Network Graphics (unlike the other formats this is a bitmap)


Schematics can also be generated from a screenshot although this is
poorer quality bitmap.


Expressions
===========

Expressions can be saved as a LaTeX representation or as a Python
script.  The latter requires Lcapy to be imported; `from lcapy import *`.

Expressions can be manipulated, transformed to another domain, and
formatted in many ways.  The select option extracts the real part,
imaginary part, etc.


Additional documentation
========================

For further information about Lcapy, see https://lcapy.readthedocs.io/

