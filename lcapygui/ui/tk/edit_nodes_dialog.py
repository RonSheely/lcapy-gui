from tkinter import Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .menu import MenuDropdown, MenuItem
from .window import Window

class EditNodesDialog(Window):

    def __init__(self, ui, update=None, title='Component nodes'):

        super(EditNodesDialog, self).__init__(ui, None, title)

        self.circuit = ui.model.circuit
        self.nodes = self.circuit.nodes
        self.update = update

        entries = []
        for key in self.nodes:
            entries.append(LabelEntry(key, key, ''))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="OK",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        changes = []
        for node in self.circuit.nodes.values():
            val = self.labelentries.get(node.name)
            if val != '':
                changes.append((node, val))

        nodes = self.circuit.nodes

        for change in changes:
            node, val = change
            node.name = val

        self.update(None)
        self.on_close()
