from tkinter import Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .menu import MenuDropdown, MenuItem
from .window import Window

# Perhaps iterate over components and annotate values;
# value, v0, phi, omega etc.
# But what about symbols used as component args?
# Better to iterate over undefined symbols in circuit.
# circuit.symbols returns all the symbols in the context;
# this includes domain vars and delta_t etc.


# Workaround for older version of Lcapy
def undefined_symbols(cct):

    from lcapy import expr

    symbols = []
    for k, elt in cct.elements.items():
        cpt = elt.cpt
        for arg in cpt.args:
            symbols += expr(arg).symbols

    return symbols


class EditValuesDialog(Window):

    def __init__(self, ui, title='Component values'):

        super(EditValuesDialog, self).__init__(ui, None, title)

        self.circuit = ui.model.circuit
        try:
            self.symbols = self.circuit.undefined_symbols
        except:
            self.symbols = undefined_symbols(self.circuit)

        menudropdowns = [
            MenuDropdown('File', 0,
                         [MenuItem('Load', self.on_load),
                          ])]

        self.add_menu(menudropdowns)

        entries = []
        for key in self.symbols:
            entries.append(LabelEntry(key, key, ''))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="OK",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        defs = {}
        for key in self.symbols:
            val = self.labelentries.get(key)
            if val == '':
                continue
            defs[key] = float(val)

        cct = self.circuit.subs(defs)

        self.ui.model.on_show_new_circuit(cct)
        self.on_close()

    def on_load(self, arg):

        pathname = self.ui.open_file_dialog(doc='Definitions', ext='.csv')

        defs = {}
        with open(pathname) as f:
            for line in f.readlines():
                if ',' in line:
                    delim = ','
                else:
                    delim = ' '
                parts = line.split(delim)
                if len(parts) != 2:
                    raise ValueError(
                        'Need comma or space separated definitions')
                name = parts[0].strip()
                value = float(parts[1].strip())
                defs[name] = value

        cct = self.circuit.subs(defs)

        self.ui.model.on_show_new_circuit(cct)
