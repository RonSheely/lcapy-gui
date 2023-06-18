from tkinter import Tk, Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries


class SubsDialog:

    def __init__(self, expr, ui, title='Substitution'):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title(title)

        entries = []

        self.symbols = []
        for key in expr.symbols:
            # Ignore domain variable
            if key != expr.var.name:
                entries.append(LabelEntry(key, key, 0.0))
                self.symbols.append(key)

        self.labelentries = LabelEntries(self.window, ui, entries)

        button = Button(self.window, text="Subs",
                        command=self.on_update)
        button.grid(row=self.labelentries.row)

    def on_update(self):

        self.window.destroy()

        defs = {}
        for key in self.symbols:
            val = self.labelentries.get_text(key)
            if val == '':
                self.ui.show_error_dialog('Undefined symbol ' + key)
                return
            val = self.labelentries.get(key)
            defs[key] = val

        expr = self.expr.subs(defs)
        self.ui.show_expr_dialog(expr)
