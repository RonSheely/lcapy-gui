from tkinter import Tk
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .expr_calc import ExprCalc


class FormatDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.master = Tk()
        self.master.title('Format')

        self.format = ''

        self.formats = {'': '',
                        'Canonical': 'canonical',
                        'Standard': 'standard',
                        'ZPK': 'ZPK',
                        'Partial fraction': 'partfrac',
                        'Time constant': 'timeconst'}

        entries = [LabelEntry('format', 'Format', self.format,
                              list(self.formats.keys()), self.on_format)]

        self.labelentries = LabelEntries(self.master, ui, entries)

    def on_format(self, fmt):

        self.master.destroy()

        if fmt == self.format:
            return
        self.format = fmt

        e = ExprCalc(self.expr)

        method = self.formats[fmt]
        if method == '':
            return

        try:
            expr = e.method(method)
            self.ui.show_expr_advanced_dialog(expr)
        except Exception as e:
            print('Ooops for %s' % method)
