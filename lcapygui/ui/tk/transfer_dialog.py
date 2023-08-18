from tkinter import Button
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class TransferFunctionDialog(Window):

    def __init__(self, ui):

        super().__init__(ui, None, 'Transfer function')

        entries = []

        names = ui.model.circuit.cpts

        entries.append(LabelEntry('input', 'Input',
                                  names[0], names))

        entries.append(LabelEntry('output', 'Output',
                                  names[0], names))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_ok(self):

        input_cpt = self.labelentries.get('input')
        output_cpt = self.labelentries.get('output')

        print(input_cpt, output_cpt)

        self.on_close()
