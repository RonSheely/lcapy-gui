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

        button = Button(self.master, text="Plot", command=self.on_plot)
        button.grid(row=1, sticky='w')

        button = Button(self.master, text="Advanced", command=self.on_advanced)
        button.grid(row=1, column=1, sticky='w')

        button = Button(self.master, text="Simplify", command=self.on_simplify)
        button.grid(row=1, column=2, sticky='w')

        self.update()

    def update(self):

        try:
            self.show_img(self.expr)
        except Exception as e:
            self.expr_label.config(text=e)

    def show_img(self, e):

        png_filename = ExprImage(e).image()
        img = ImageTk.PhotoImage(Image.open(png_filename), master=self.master)
        self.expr_label.config(image=img)
        self.expr_label.photo = img

    def on_plot(self):

        if not isinstance(self.expr, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr)

    def on_advanced(self):

        self.ui.show_expr_advanced_dialog(self.expr, self.title)

    def on_simplify(self):

        self.expr = self.expr.simplify()
        self.update()
