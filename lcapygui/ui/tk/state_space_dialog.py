from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class TransferFunctionDialog:

    def __init__(self, ui, cpt):

        self.ui = ui
        self.master = Tk()
        self.master.title('State space')
        self.ss = ui.model.circuit.ss
        self.kindmap = {'State matrix, A': 'A',
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
                        'System impulse responses matrix, h': 'h'}

        entries = []
        kinds = list(self.kindmap.keys())

        entries.append(LabelEntry('kind', 'Aspect', kinds[0], kinds,
                                  self.on_update))

        self.labelentries = LabelEntries(self.master, ui, entries)

    def on_update(self, foo):

        kind = self.labelentries.get('kind')

        self.ui.show_expr_dialog(getattr(self.ss, self.kindmap[kind]), kind)
