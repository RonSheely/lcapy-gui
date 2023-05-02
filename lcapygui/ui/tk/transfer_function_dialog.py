from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class TransferFunctionDialog:

    def __init__(self, ui, cpt):

        self.ui = ui
        self.master = Tk()
        self.master.title('Transfer function')

        entries = []

        elements = ui.model.circuit.elements
        names = [elt.name for elt in elements.values()
                 if elt.type not in ('W', 'O')]

        entries.append(LabelEntry('input', 'Input',
                                  names[0], names))

        entries.append(LabelEntry('output', 'Output',
                                  names[-1], names))

        entries.append(LabelEntry('kind', 'Kind', 'Voltage ratio',
                                  ['Voltage ratio', 'Current ratio',
                                   'Transimpedance',
                                   'Transadmittance']))

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_ok(self):

        input_cpt = self.labelentries.get('input')
        output_cpt = self.labelentries.get('output')
        kind = self.labelentries.get('kind')

        cct = self.ui.model.circuit
        # TODO, remove independent sources

        if kind == 'Voltage ratio':
            H = cct.voltage_gain(input_cpt, output_cpt)
        elif kind == 'Current ratio':
            H = cct.current_gain(input_cpt, output_cpt)
        elif kind == 'Transimpedance':
            H = cct.transimpedance(input_cpt, output_cpt)
        elif kind == 'Transadmittance':
            H = cct.transadmittance(input_cpt, output_cpt)
        else:
            raise ValueError('Unknown kind')

        self.ui.show_expr_dialog(H, kind)

        self.master.destroy()
