from tkinter import StringVar, Label, Entry, Button
from .window import Window


class NodePropertiesDialog(Window):

    def __init__(self, ui, node, update=None, title=''):

        # FIXME if have node name same as a cpt name
        super(NodePropertiesDialog, self).__init__(ui, node.name, title)

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

        button = Button(self, text="OK", command=self.on_ok)
        button.grid(row=row)

    def on_ok(self):

        node_name = self.name_var.get()

        if self.node.name != node_name and self.update:
            self.node.name = node_name
            self.update(self.node)

        self.on_close()
