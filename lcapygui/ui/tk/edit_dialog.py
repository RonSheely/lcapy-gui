from tkinter import Tk, Entry, Button, StringVar
from lcapy import expr


class EditDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title('Expression editor')

        self.var = StringVar(self.window)
        self.var.set(str(expr))

        self.entry = Entry(self.window, textvariable=self.var)
        self.entry.grid(row=0)

        button = Button(self.window, text="Show", command=self.on_show)
        button.grid(row=1)

    def on_show(self):

        expr_str = self.var.get()

        try:
            self.ui.show_expr_dialog(expr(expr_str))
            self.window.destroy()

        except Exception as e:
            self.ui.show_error_dialog('Cannot evaluate expression')
