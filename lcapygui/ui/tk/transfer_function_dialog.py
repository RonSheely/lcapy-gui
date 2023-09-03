from tkinter import Button
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class TransferFunctionDialog(Window):

    def __init__(self, ui, cpt):

        super().__init__(ui, None, 'Transfer function')

        entries = []

        elements = ui.model.circuit.elements

        # TODO, allow V or I
        names = [elt.name for elt in elements.values()
                 if elt.type not in ('W', 'O', 'V', 'I')]

        entries.append(LabelEntry('input', 'Input',
                                  names[0], names))

        entries.append(LabelEntry('output', 'Output',
                                  names[-1], names))

        entries.append(LabelEntry('kind', 'Kind', 'Voltage ratio',
                                  ['Voltage ratio', 'Current ratio',
                                   'Transimpedance',
                                   'Transadmittance']))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="Show", command=self.on_show)
        button.grid(row=self.labelentries.row)

    def on_show(self):

        input_cpt = self.labelentries.get('input')
        output_cpt = self.labelentries.get('output')
        kind = self.labelentries.get('kind')

        # Remove independent sources
        cct = self.ui.model.circuit
        cct = cct.copy()
        values = list(cct.elements.values())
        for cpt in values:
            if cpt.is_independent_source:
                cct.remove(cpt.name)

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
