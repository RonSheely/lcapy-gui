from tkinter import Tk
from tkinter.ttk import Button, Label, Frame
from PIL import Image, ImageTk
from lcapy import Expr
from .exprimage import ExprImage


global_dict = {}
exec('from lcapy import *', global_dict)


class ExprAdvancedDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.ui = ui

        # Perhaps show full expr string?
        self.expression = 'result'

        self.master = Tk()
        self.master.title(title)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=0)

        button_frame = Frame(self.master)
        button_frame.grid(row=1, column=0, sticky='w')

        button = Button(button_frame, text="Plot", command=self.on_plot)
        button.grid(row=0, column=0, sticky='w')

        button = Button(button_frame, text="LaTeX", command=self.on_latex)
        button.grid(row=0, column=1, sticky='w')

        button = Button(button_frame, text="Python", command=self.on_python)
        button.grid(row=0, column=2, sticky='w')

        button = Button(button_frame, text="Attributes",
                        command=self.on_attributes)
        button.grid(row=0, column=3, sticky='w')

        button = Button(button_frame, text="Simplify",
                        command=self.on_simplify)
        button.grid(row=0, column=4, sticky='w')

        button = Button(button_frame, text="Approximate",
                        command=self.on_approximate)
        button.grid(row=0, column=5, sticky='w')

        button = Button(button_frame, text="Transform",
                        command=self.on_transform)
        button.grid(row=0, column=6, sticky='w')

        button = Button(button_frame, text="Format",
                        command=self.on_format)
        button.grid(row=0, column=7, sticky='w')

        button = Button(button_frame, text="Edit",
                        command=self.on_edit)
        button.grid(row=0, column=8, sticky='w')

        self.update()

    def update(self):

        try:
            self.show_img(self.expr)
        except Exception as e:
            self.expr_label.config(text=e)

    def show_pretty(self, e):

        self.expr_label.config(text=e.pretty())

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

    def on_latex(self):

        self.ui.show_message_dialog(self.expr.latex())

    def on_python(self):

        e = self.expr

        s = ''
        for sym in e.symbols:
            # Skip domain variables
            if sym in ('f', 's', 't', 'w', 'omega',
                       'jf', 'jw', 'jomega', 'n', 'k', 'z'):
                continue

            # TODO, add assumptions
            s += "%s = symbol('%s')\n" % (sym, sym)
        # TODO, fix Lcapy to provide static classes
        s += repr(e)

        self.ui.show_message_dialog(s, 'Python expression')

    def on_attributes(self):
        # TODO
        pass

    def on_simplify(self):

        expr = self.expr.simplify()
        # Perhaps have simplify dialog?
        self.ui.show_expr_advanced_dialog(expr)

    def on_approximate(self):

        self.ui.show_approximate_dialog(self.expr)

    def on_transform(self):

        self.ui.show_transform_dialog(self.expr)

    def on_format(self):

        self.ui.show_format_dialog(self.expr)

    def on_edit(self):
        # TODO
        self.ui.show_edit_dialog(self.expr)
