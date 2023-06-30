from tkinter import Tk, Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries

# Perhaps iterate over components and annotate values;
# value, v0, phi, omega etc.
# But what about symbols used as component args?
# Better to iterate over undefined symbols in circuit.
# circuit.symbols returns all the symbols in the context;
# this includes domain vars and delta_t etc.


class EditValuesDialog:

    def __init__(self, ui, title='Component values'):

        self.ui = ui
        self.window = Tk()
        self.window.title(title)
        self.circuit = ui.model.circuit
        self.symbols = self.circuit.undefined_symbols

        entries = []
        for key in self.symbols:
            entries.append(LabelEntry(key, key, ''))

        self.labelentries = LabelEntries(self.window, ui, entries)

        button = Button(self.window, text="OK",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        self.window.destroy()

        defs = {}
        for key in self.symbols:
            val = self.labelentries.get(key)
            if val == '':
                continue
            defs[key] = float(val)

        cct = self.circuit.subs(defs)

        self.ui.model.on_show_new_circuit(cct)
