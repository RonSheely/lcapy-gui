from tkinter import Tk, Button, Label
from PIL import Image, ImageTk

from lcapy import Expr
from .exprimage import ExprImage


global_dict = {}
exec('from lcapy import *', global_dict)


class ExprDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.ui = ui
        self.labelentries = None
        self.title = title

        self.master = Tk()
        self.master.title(title)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=0, columnspan=4)

        ops = {'Simplify': 'simplify',
               ', B': 'B',

        button = Button(self.master, text="Plot", command=self.on_plot)
        button.grid(row=1, sticky='w')

        button = Button(self.master, text="Advanced", command=self.on_advanced)
        button.grid(row=1, column=1, sticky='w')

        button = Button(self.master, text="Simplify", command=self.on_simplify)
        button.grid(row=1, column=2, sticky='w')

        button = Button(self.master, text="Python", command=self.on_python)
        button.grid(row=1, column=3, sticky='w')

        button = Button(self.master, text="LaTeX", command=self.on_latex)
        button.grid(row=1, column=4, sticky='w')

        self.update()

    def update(self):

        try:
            self.show_img(self.expr)
        except Exception as e:
            self.expr_label.config(text=e)

    def show_img(self, e):

        # TODO, fixme
        # if self.ui.model.preferences.show_units == 'true':
        #    e = e * e.units

        png_filename = ExprImage(e).image()
        img = ImageTk.PhotoImage(Image.open(png_filename), master=self.master)
        self.expr_label.config(image=img)
        self.expr_label.photo = img

    def on_advanced(self):

        self.ui.show_expr_advanced_dialog(self.expr, self.title)

    def on_plot(self):

        if not isinstance(self.expr, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr)

    def on_python(self):

        s = ''
        for sym in self.expr.symbols:
            # Skip domain variables
            if sym in ('f', 's', 't', 'w', 'omega',
                       'jf', 'jw', 'jomega', 'n', 'k', 'z'):
                continue

            # TODO, add assumptions
            s += "%s = symbol('%s')\n" % (sym, sym)
        # TODO, fix Lcapy to provide static classes
        s += repr(self.expr)

        self.ui.show_message_dialog(s, 'Python expression')

    def on_simplify(self):

        self.expr = self.expr.simplify()
        self.update()

    def on_latex(self):

        self.ui.show_message_dialog(self.expr_tweak.latex())
