from tkinter import Tk, StringVar, Label, Entry, Button

# Perhaps add subplots, each of a specific domain with specified
# min and max x and y values.
# Best to not allow overplotting of different quantities (v and i, etc.)
# Maybe specify domain and quantity (time, voltage) then specify
# components (or perhaps nodes)
# Could have a fixed number for the maximum number of plots, say 8
# and then have 8 dropdown lists.


class MultiplotDialog:

    def __init__(self, ui):

        self.ui = ui

        self.window = Tk()

        circuit = ui.model.circuit

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

        button = Button(self.window, text="OK", command=self.on_update)
        button.grid(row=row)

    def on_update(self):

        self.window.destroy()
