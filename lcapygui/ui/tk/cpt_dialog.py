from tkinter import StringVar, Label, OptionMenu, Entry, Button
from ..components import Capacitor, Inductor
from .window import Window


class CptDialog(Window):

    def __init__(self, cpt, update=None):

        super().__init__(None, None, cpt.name)

        self.cpt = cpt
        self.update = update

        row = 0

        self.kind_var = None
        if cpt.kind is not None:
            self.kind_var = StringVar(self)
            self.kind_var.set(cpt.kind)

            kind_label = Label(self, text='Kind: ')
            kind_option = OptionMenu(self, self.kind_var,
                                     *cpt.kinds.keys())

            kind_label.grid(row=row)
            kind_option.grid(row=row, column=1)
            row += 1

        self.name_var = StringVar(self)
        self.name_var.set(cpt.name)

        name_label = Label(self, text='Name: ')
        name_entry = Entry(self, textvariable=self.name_var,
                           command=self.on_update)

        name_label.grid(row=row)
        name_entry.grid(row=row, column=1)
        row += 1

        self.value_var = StringVar(self)
        value = cpt.value
        if value is None:
            value = cpt.name
        self.value_var.set(value)

        value_label = Label(self, text='Value: ')
        value_entry = Entry(self, textvariable=self.value_var,
                            command=self.on_update)

        value_label.grid(row=row)
        value_entry.grid(row=row, column=1)
        row += 1

        self.initial_value_var = None
        if isinstance(cpt, (Capacitor, Inductor)):

            ivlabel = 'v0'
            if isinstance(cpt, Inductor):
                ivlabel = 'i0'

            self.initial_value_var = StringVar(self)

            initial_value_label = Label(self, text=ivlabel + ': ')
            initial_value_entry = Entry(
                self, textvariable=self.initial_value_var,
                command=self.on_update)
            initial_value_label.grid(row=row)
            initial_value_entry.grid(row=row, column=1)
            row += 1

        button = Button(self, text="OK", command=self.on_ok)
        button.grid(row=row)

    def on_update(self, arg=None):

        if self.kind_var is not None:
            kind = self.kind_var.get()
            if kind == '':
                kind = None
            self.cpt.kind = kind

        self.cpt.name = self.name_var.get()

        value = self.value_var.get()
        if value == '':
            value = None
        self.cpt.value = value

        if self.initial_value_var is not None:
            value = self.initial_value_var.get()
            if value == '':
                value = None
            self.cpt.initial_value = value

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.on_close()
