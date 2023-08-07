from tkinter import StringVar, Label, Entry, Button
from .window import Window

# Perhaps add subplots, each of a specific domain with specified
# min and max x and y values.
# Best to not allow overplotting of different quantities (v and i, etc.)
# Maybe specify domain and quantity (time, voltage) then specify
# components (or perhaps nodes)
# Could have a fixed number for the maximum number of plots, say 8
# and then have 8 dropdown lists.   This is probably easier than having a
# menu item for adding another plot.
# But also need a way to handle multiple subplots (these are not overdrawn)
# Could have a specified number of rows and cols for the subplot grid.

# Automatically add labels, R1 voltage, C1 current, etc.
# Perhaps allow expressions, R1.V(t) - R2.V(t)?

# What about real part, magnitude, phase etc?
# Could use expression such as R1.V(f).phase

# Expression  row  col  xmin  xmax  ymin  ymax colour style


class MultiplotDialog(Window):

    def __init__(self, ui):

        super().__init__(ui, None, '')

        circuit = ui.model.circuit

        # TODO: need undefined_symbols for old Lcapy
        symbols = circuit.undefined_symbols
        if symbols != []:
            ui.show_error_dialog(
                'Undefined symbols: %s.  Use edit values to define' % ', '.join(symbols))

        elements = circuit.elements

        entries = []
        for elt in elements:
            # TODO
            print(elt)

        row = 0

        # R1  voltage  domain

        button = Button(self, text="OK", command=self.on_update)
        button.grid(row=row)

    def on_update(self):

        self.on_close()
