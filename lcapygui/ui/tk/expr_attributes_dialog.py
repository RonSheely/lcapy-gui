from tkinter import Tk
from .labelentries import LabelEntry, LabelEntries


class ExprAttributesDialog:

    def __init__(self, expr, ui, title='Expression attributes'):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title(title)

        entries = [LabelEntry('units', 'Units', expr.units),
                   LabelEntry('domain', 'Domain', expr.domain),
                   LabelEntry('quantity', 'Quantity', expr.quantity),
                   LabelEntry('causal', 'Causal', expr.is_causal, command=self.causal)]

        self.labelentries = LabelEntries(self.window, ui, entries)

    def causal(self):

        self.expr.is_causal = self.labelentries.get('causal')
