from tkinter import Tk, Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries


class ApproximateDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.master = Tk()
        self.master.title('Plot properties')

        entries = []

        self.symbols = []
        for key in expr.symbols:
            # Ignore domain variable
            if key != expr.var.name:
                entries.append(LabelEntry(key, key, 0.0))
                self.symbols.append(key)

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="Approximate",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        self.master.destroy()

        defs = {}
        for key in self.symbols:
            val = self.labelentries.get_text(key)
            if val == '':
                self.ui.show_error_dialog('Undefined symbol ' + key)
                return
            val = self.labelentries.get(key)
            defs[key] = val

        expr = self.expr.approximate_dominant(defs)
        self.ui.show_expr_advanced_dialog(expr)
