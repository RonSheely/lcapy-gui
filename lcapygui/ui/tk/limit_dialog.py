from tkinter import Button
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class LimitDialog(Window):

    def __init__(self, expr, ui, title='Limit'):

        super().__init__(ui, None, title)

        self.expr = expr

        symbols = list(expr.symbols)
        if len(symbols) == 0:
            raise ValueError('Constant expression')

        entries = []
        entries.append(LabelEntry('symbol', 'symbol',
                                  symbols[0], symbols))

        entries.append(LabelEntry('limit', 'Limit', '0'))

        entries.append(LabelEntry('dir', 'Direction',
                                  '+', ('+', '-')))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_ok(self):

        symbol = self.labelentries.get('symbol')
        limit = self.labelentries.get('limit')
        dir = self.labelentries.get('dir')

        expr = self.expr.limit(symbol, limit, dir)
        self.ui.show_expr_dialog(expr)

        self.on_close()
