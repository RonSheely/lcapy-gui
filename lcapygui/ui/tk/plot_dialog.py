from tkinter import StringVar, Label, Entry, Button
from .window import Window


class PlotDialog(Window):

    def __init__(self, node, update=None):

        super().__init__(None, None, 'Plot dialog')

        self.node = node
        self.update = update

        row = 0

        self.name_var = StringVar(self)
        self.name_var.set(node.name)

        name_label = Label(self, text='Name: ')
        name_entry = Entry(self, textvariable=self.name_var)

        name_label.grid(row=row)
        name_entry.grid(row=row, column=1)
        row += 1

        button = Button(self, text="OK", command=self.on_update)
        button.grid(row=row)

    def on_update(self):

        self.node.name = self.name_var.get()

        if self.update:
            self.update(self.node)

        self.on_close()
