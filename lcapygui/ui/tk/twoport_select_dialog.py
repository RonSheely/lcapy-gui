from tkinter import Button
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class TwoportSelectDialog(Window):

    def __init__(self, ui, TP, model):

        super().__init__(ui, None, 'Twoport')

        self.TP = TP

        models = ('A', 'B', 'G', 'H', 'S', 'T', 'Y', 'Z')
        elements = ('matrix', '11', '12', '21', '22')

        entries = []
        entries.append(LabelEntry('model', 'Twoport model',
                                  model, models))
        entries.append(LabelEntry('element', 'Twoport element',
                                  elements[0], elements))

        self.labelentries = LabelEntries(self, ui, entries)

        button = Button(self, text="Show", command=self.on_show)
        button.grid(row=self.labelentries.row)

    def on_show(self):

        model = self.labelentries.get('model')
        element = self.labelentries.get('element')
        TP = self.TP

        if model == 'A':
            if element == 'matrix':
                expr = TP.Aparams
            elif element == '11':
                expr = TP.A11
            elif element == '12':
                expr = TP.A12
            elif element == '21':
                expr = TP.A21
            elif element == '22':
                expr = TP.A22
        elif model == 'B':
            if element == 'matrix':
                expr = TP.Bparams
            elif element == '11':
                expr = TP.B11
            elif element == '12':
                expr = TP.B12
            elif element == '21':
                expr = TP.B21
            elif element == '22':
                expr = TP.B22
        elif model == 'G':
            if element == 'matrix':
                expr = TP.Gparams
            elif element == '11':
                expr = TP.G11
            elif element == '12':
                expr = TP.G12
            elif element == '21':
                expr = TP.G21
            elif element == '22':
                expr = TP.G22
        elif model == 'H':
            if element == 'matrix':
                expr = TP.Hparams
            elif element == '11':
                expr = TP.H11
            elif element == '12':
                expr = TP.H12
            elif element == '21':
                expr = TP.H21
            elif element == '22':
                expr = TP.H22
        elif model == 'S':
            if element == 'matrix':
                expr = TP.Sparams
            elif element == '11':
                expr = TP.S11
            elif element == '12':
                expr = TP.S12
            elif element == '21':
                expr = TP.S21
            elif element == '22':
                expr = TP.S22
        elif model == 'T':
            if element == 'matrix':
                expr = TP.Tparams
            elif element == '11':
                expr = TP.T11
            elif element == '12':
                expr = TP.T12
            elif element == '21':
                expr = TP.T21
            elif element == '22':
                expr = TP.T22
        elif model == 'Y':
            if element == 'matrix':
                expr = TP.Yparams
            elif element == '11':
                expr = TP.Y11
            elif element == '12':
                expr = TP.Y12
            elif element == '21':
                expr = TP.Y21
            elif element == '22':
                expr = TP.Y22
        elif model == 'Z':
            if element == 'matrix':
                expr = TP.Zparams
            elif element == '11':
                expr = TP.Z11
            elif element == '12':
                expr = TP.Z12
            elif element == '21':
                expr = TP.Z21
            elif element == '22':
                expr = TP.Z22

        name = model + element

        self.ui.show_expr_dialog(expr, title=name)
