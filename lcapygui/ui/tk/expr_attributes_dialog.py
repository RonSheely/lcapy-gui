from tkinter import Tk
from .labelentries import LabelEntry, LabelEntries


class ExprAttributesDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title('Expression attributes')

        entries = [LabelEntry('units', 'Units', expr.units),
                   LabelEntry('domain', 'Domain', expr.domain),
                   LabelEntry('quantity', 'Quantity', expr.quantity)]

        self.labelentries = LabelEntries(self.window, ui, entries)
