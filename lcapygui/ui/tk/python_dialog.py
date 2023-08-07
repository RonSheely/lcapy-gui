from tkinter import Entry, Button, Text, BOTH, END
from lcapy import expr
from re import sub
from .window import Window

global_dict = {}
exec('from lcapy import *', global_dict)


def exec_function(expr):

    lines = expr.split('\n')
    lines[-1] = 'return ' + lines[-1]
    s = '\n'.join(lines)

    context = {}
    local_vars = {}

    s = sub(r"(?m)^", "    ", s)
    s = "def _anon():\n" + s

    exec(s, global_dict, context)
    result = context['_anon']()

    return result


class PythonDialog(Window):

    def __init__(self, expr, ui):

        super().__init__(ui, None, 'Expression editor')

        self.expr = expr

        symbols = self.expr.symbols

        s = ''
        for sym in symbols:
            # Skip domain variables
            if sym in ('f', 's', 't', 'w', 'omega',
                       'jf', 'jw', 'jomega', 'n', 'k', 'z'):
                continue

            # TODO, add other assumptions
            if symbols[sym].is_positive:
                s += "%s = symbol('%s', positive=True)\n" % (sym, sym)
            else:
                s += "%s = symbol('%s')\n" % (sym, sym)

        s += repr(self.expr)

        self.text = Text(self)
        self.text.pack(fill=BOTH, expand=1)
        self.text.insert(END, s)

        button = Button(self, text='Show', command=self.on_show)
        button.pack()

    def on_show(self):

        expr_str = self.text.get('1.0', END).strip()

        try:
            expr = exec_function(expr_str)
            self.ui.show_expr_dialog(expr)
            self.on_close()

        except Exception as e:
            self.ui.show_error_dialog('Cannot evaluate expression')
