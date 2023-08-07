from tkinter import Button
from .window import Window


class InspectDialog(Window):

    def __init__(self, ui, cpt, title=''):

        super().__init__(ui, None, title)

        self.model = ui.model
        self.cpt = cpt

        buttons = [('Voltage', self.on_voltage),
                   ('Current', self.on_current),
                   ('Component impedance', self.on_impedance),
                   ('Component admittance', self.on_admittance),
                   ('Thevenin impedance', self.on_thevenin_impedance),
                   ('Norton admittance', self.on_norton_admittance)]
        for b in buttons:
            button = Button(self, text=b[0], command=b[1])
            button.pack()

    def on_voltage(self):

        self.model.inspect_voltage(self.cpt)

    def on_current(self):

        self.model.inspect_current(self.cpt)

    def on_impedance(self):

        self.model.inspect_impedance(self.cpt)

    def on_admittance(self):

        self.model.inspect_admittance(self.cpt)

    def on_thevenin_impedance(self):

        self.model.inspect_thevenin_impedance(self.cpt)

    def on_norton_admittance(self):

        self.model.inspect_norton_admittance(self.cpt)
