from tkinter import Tk, Entry, Button, StringVar
from lcapy import expr


class EditDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.master = Tk()
        self.master.title('Expression editor')

        self.var = StringVar(self.master)
        self.var.set(str(expr))

        self.entry = Entry(self.master, textvariable=self.var, width=50)
        self.entry.grid(row=0)

        button = Button(self.master, text="Show", command=self.on_show)
        button.grid(row=1)

    def on_show(self):

        expr_str = self.var.get()

        try:
            self.ui.show_expr_advanced_dialog(expr(expr_str))
            self.master.destroy()

        except Exception as e:
            self.ui.show_error_dialog('Cannot evaluate expression')
