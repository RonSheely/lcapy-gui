from tkinter import Tk, Entry, Button, Text, BOTH, END
from lcapy import expr


class EditDialog:

    def __init__(self, expr, ui):

        self.expr = expr
        self.ui = ui

        self.window = Tk()
        self.window.title('Expression editor')

        s = str(expr)

        self.text = Text(self.window)
        self.text.pack(fill=BOTH, expand=1)
        self.text.insert(END, s)

        button = Button(self.window, text='Show', command=self.on_show)
        button.pack()

    def on_show(self):

        expr_str = self.text.get('1.0', END).strip()

        try:
            self.ui.show_expr_dialog(expr(expr_str))
            self.window.destroy()

        except Exception as e:
            self.ui.show_error_dialog('Cannot evaluate expression')
