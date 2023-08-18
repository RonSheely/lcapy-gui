Adding new components
=====================

If the component is known to Lcapy (see `lcapy.schemcpts.py`):

1. Create a file in `lcapygui/components` and add new component class.
   For example, add `Foo` in `foo.py`.  If it is a bipole use
   `resistor.py` as a template.

2. Add component to component_map in `lcapygui/ui/uimodelbase.py`

3. Add component to cpts in `lcapgui/cpt_maker.py` and import class

4. Create an SVG file by importing make from makesvg and calling it
   with the component type, e.g., `make('R')`

5. Add the new SVG file in `lcapygui/data/svg/` to git

6. Install `lcapy-gui` (to copy new SVG file to correct location)

7. Run `sketchview` to view the SVG file.  Use the `--pins` option to
   show the pins.

8. Define the pin locations in `foo.py`; zoom in to the displayed SVG
   file to find the exact locations.

9. Update the menu in `lcapygui/ui/tk/uimodelmph.py`
