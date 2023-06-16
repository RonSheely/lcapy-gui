from tkinter import Tk
from .labelentries import LabelEntry, LabelEntries


class ExprAttributesDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.master = Tk()
        self.master.title('Expression attributes')

        entries = [LabelEntry('units', 'Units', expr.units),
                   LabelEntry('domain', 'Domain', expr.domain),
                   LabelEntry('quantity', 'Quantity', expr.quantity)]

        self.labelentries = LabelEntries(self.master, ui, entries)
