from tkinter import Button
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class TwoportDialog(Window):

    def __init__(self, ui, cpt, kind):

        super().__init__(ui, None, 'Twoport')

        self.kind = kind

        entries = []

        elements = ui.model.circuit.elements

        # TODO, allow V or I
        names = [elt.name for elt in elements.values()
                 if elt.type not in ('W', 'O', 'V', 'I')]

        entries.append(LabelEntry('input', 'Input',
                                  names[0], names))

        entries.append(LabelEntry('output', 'Output',
                                  names[-1], names))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="Create", command=self.on_create)
        button.grid(row=self.labelentries.row)

        self.minsize(200, 50)

    def on_create(self):

        input_cpt = self.labelentries.get('input')
        output_cpt = self.labelentries.get('output')

        # Remove independent sources
        cct = self.ui.model.circuit
        cct = cct.copy()
        values = list(cct.elements.values())
        for cpt in values:
            if cpt.is_independent_source:
                cct.remove(cpt.name)

        # Warn that might be slow
        A = cct.twoport(input_cpt, output_cpt, model=self.kind)

        self.ui.show_twoport_select_dialog(A, self.kind)
