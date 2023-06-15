from tkinter import Tk
from numpy import linspace
from .labelentries import LabelEntry, LabelEntries
from .expr_calc import ExprCalc


class TransformDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.master = Tk()
        self.master.title('Transform')

        self.domains = {'': '',
                        'Time': 'time',
                        'Phasor': 'phasor',
                        'Laplace': 'laplace',
                        'Fourier': 'fourier',
                        'Frequency': 'frequency_response',
                        'Angular Fourier': 'angular_fourier',
                        'Angular Frequency': 'angular_frequency_response'}

        try:
            self.domain = next(key for key, value in self.domains.items()
                               if value == expr.domain)
        except Exception:
            self.domain = ''

        entries = [LabelEntry('domain', 'Domain', self.domain,
                              list(self.domains.keys()), self.on_domain)]

        self.labelentries = LabelEntries(self.master, ui, entries)

    def on_domain(self, domain):

        self.master.destroy()

        if domain == self.domain:
            return
        self.domain = domain

        e = ExprCalc(self.expr)

        method = self.domains[domain]
        if method == '':
            return

        try:
            expr = e.method(method)
            self.ui.show_expr_advanced_dialog(expr)
        except Exception as e:
            print('Ooops for %s' % method)
