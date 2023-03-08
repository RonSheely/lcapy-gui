Adding new components
=====================

If the component is known to Lcapy (see lcapy.schemcpts.py):

1. Create a file in lcapygui/components.  If it is a bipole use
   resistor.py as a template.

2. Add component to component_map in lcapygui/uimodelbase.py

3. Add component to cpts in lcapgui/cpt_maker.py and import class

4. Create an SVG file by importing make from makesvg and calling it
   with the component type.

5. Add the new SVG file to git

6. Install lcapy-gui (to copy new SVG file to correct location)
