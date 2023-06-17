from tkinter import Tk, StringVar, Label, Entry, Button


class PlotDialog:

    def __init__(self, node, update=None):

        self.node = node
        self.update = update

        self.window = Tk()

        row = 0

        self.name_var = StringVar(self.window)
        self.name_var.set(node.name)

        name_label = Label(self.window, text='Name: ')
        name_entry = Entry(self.window, textvariable=self.name_var)

        name_label.grid(row=row)
        name_entry.grid(row=row, column=1)
        row += 1

        button = Button(self.window, text="OK", command=self.on_update)
        button.grid(row=row)

    def on_update(self):

        self.node.name = self.name_var.get()

        self.window.destroy()

        if self.update:
            self.update(self.node)
