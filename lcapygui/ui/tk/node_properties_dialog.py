from tkinter import Tk, StringVar, Label, Entry, Button


class NodePropertiesDialog:

    def __init__(self, ui, node, update=None, title=''):

        self.ui = ui
        self.node = node
        self.update = update

        self.window = Tk()
        self.window.title(title)

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

    def focus(self):

        # Put window on top
        self.window.attributes('-topmost', True)
        self.window.focus()

    def on_close(self):

        self.ui.dialogs.pop(self.cpt.name)
        self.window.destroy()

    def on_update(self):

        node_name = self.name_var.get()

        self.window.destroy()

        if self.node.name != node_name and self.update:
            self.node.name = node_name
            self.update(self.node)
