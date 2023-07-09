from tkinter import Tk, Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries


class LimitDialog:

    def __init__(self, expr, ui, title='Limit'):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title(title)

        symbols = list(expr.symbols)
        if len(symbols) == 0:
            raise ValueError('Constant expression')

        entries = []
        entries.append(LabelEntry('symbol', 'symbol',
                                  symbols[0], symbols))

        entries.append(LabelEntry('limit', 'Limit', 0.0))

        entries.append(LabelEntry('dir', 'Direction',
                                  '+', ('+', '-')))

        self.labelentries = LabelEntries(self.window, ui, entries)

        button = Button(self.window, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_ok(self):

        self.window.destroy()

        symbol = self.labelentries.get('symbol')
        limit = self.labelentries.get('limit')
        dir = self.labelentries.get('dir')

        expr = self.expr.limit(symbol, limit, dir)
        self.ui.show_expr_dialog(expr)
