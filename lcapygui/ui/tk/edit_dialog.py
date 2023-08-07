from tkinter import Entry, Button, Text, BOTH, END
from lcapy import expr
from .window import Window


class EditDialog(Window):

    def __init__(self, ui, expr):

        super().__init__(ui, None, 'Expression editor')

        self.expr = expr

        s = str(expr)

        self.text = Text(self)
        self.text.pack(fill=BOTH, expand=1)
        self.text.insert(END, s)

        button = Button(self, text='Show', command=self.on_show)
        button.pack()

    def on_show(self):

        expr_str = self.text.get('1.0', END).strip()

        try:
            self.ui.show_expr_dialog(expr(expr_str))
            self.on_close()

        except Exception as e:
            self.ui.show_error_dialog('Cannot evaluate expression')
