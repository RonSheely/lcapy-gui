from tkinter import Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class ApproximateDialog(Window):

    def __init__(self, expr, ui, title='Approximation'):

        super(ApproximateDialog, self).__init__(ui, None, title)

        self.expr = expr

        entries = []

        # TODO: Add label to explain to define ballpark values

        self.symbols = []
        for key in expr.symbols:
            # Ignore domain variable
            if expr.var is None or key != expr.var.name:
                entries.append(LabelEntry(key, key, key))
                self.symbols.append(key)

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="Approximate",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        defs = {}
        for key in self.symbols:
            val = self.labelentries.get_text(key)
            if val == '':
                self.ui.show_error_dialog('Undefined symbol ' + key)
                return
            val = self.labelentries.get(key)
            defs[key] = val

        expr = self.expr.approximate_dominant(defs)
        self.ui.show_expr_dialog(expr)

        self.on_close()
