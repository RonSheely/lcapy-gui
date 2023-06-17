from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class TransferFunctionDialog:

    def __init__(self, ui, cpt):

        self.ui = ui
        self.window = Tk()
        self.window.title('State space')
        self.ss = ui.model.circuit.ss
        self.kindmap = {'State equations': 'state_equations',
                        'Output equations': 'output_equations',
                        'State matrix, A': 'A',
                        'Input matrix, B': 'B',
                        'Output matrix, C': 'C',
                        'Feed through matrix, D': 'D',
                        'Transfer function vector, G': 'G',
                        'System transfer functions matrix, H': 'H',
                        'Eigenvalue matrix, Lambda': 'Lambda',
                        'Modal matrix, M': 'M',
                        'Characteristic polynomial': 'P',
                        'State transition matrix (Laplace), Phi': 'Phi',
                        'Input vector (Laplace), U': 'U',
                        'State vector (Laplace), X': 'X',
                        'Output vector (Laplace), Y': 'Y',
                        'Input vector, u': 'u',
                        'State vector, x': 'x',
                        'State initial value vector, x0': 'x0',
                        'Output vector, y': 'y',
                        'System impulse responses matrix, h': 'h',
                        'Controllability matrix': 'controllability_matrix',
                        'Observability matrix': 'observability_matrix'}

        entries = []
        kinds = list(self.kindmap.keys())

        entries.append(LabelEntry('kind', 'Aspect', kinds[0], kinds))

        self.labelentries = LabelEntries(self.window, ui, entries)

        button = Button(self.window, text="Show", command=self.on_show)
        button.grid(row=self.labelentries.row)

    def on_show(self):

        kind = self.labelentries.get('kind')

        attr = getattr(self.ss, self.kindmap[kind])
        try:
            expr = attr()
        except (AttributeError, TypeError):
            expr = attr

        self.ui.show_expr_dialog(expr)
