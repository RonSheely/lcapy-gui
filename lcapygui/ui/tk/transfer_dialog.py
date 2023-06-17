from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class TransferFunctionDialog:

    def __init__(self, ui):

        self.ui = ui
        self.window = Tk()
        self.window.title('Transfer function')

        entries = []

        names = ui.model.circuit.cpts

        entries.append(LabelEntry('input', 'Input',
                                  names[0], names))

        entries.append(LabelEntry('output', 'Output',
                                  names[0], names))

        self.labelentries = LabelEntries(self.window, ui, entries)

        button = Button(self.window, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_ok(self):

        input_cpt = self.labelentries.get('input')
        output_cpt = self.labelentries.get('output')

        print(input_cpt, output_cpt)

        self.window.destroy()
