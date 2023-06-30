from tkinter import Tk, StringVar, Label, Entry, Button


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
