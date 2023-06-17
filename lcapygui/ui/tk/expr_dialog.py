from tkinter import Tk, Button, Label
from PIL import Image, ImageTk

from lcapy import Expr
from .exprimage import ExprImage
from .expr_calc import ExprCalc
from .menu import MenuBar, MenuDropdown, MenuItem


class ExprDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.ui = ui
        self.title = title

        self.window = Tk()
        self.window.title(title)

        menudropdowns = [
            MenuDropdown('View', 0,
                         [MenuItem('Plot', self.on_plot),
                          MenuItem('LaTeX', self.on_latex),
                          MenuItem('Python', self.on_python)]),
            MenuDropdown('Edit', 0,
                         [MenuItem('Expression', self.on_edit)]),
            MenuDropdown('Format', 0,
                         [MenuItem('ZPK', self.on_format),
                          MenuItem('Canonical', self.on_format),
                          MenuItem('Time constant', self.on_format),
                          MenuItem('General', self.on_format),
                          MenuItem('Standard', self.on_format),
                          MenuItem('Partial fraction', self.on_format)]),
            MenuDropdown('Transform', 0,
                         [MenuItem('Time', self.on_transform),
                          MenuItem('Laplace', self.on_transform),
                          MenuItem('Fourier', self.on_transform)]),
            MenuDropdown('Ops', 0,
                         [MenuItem('Simplify', self.on_ops),
                          MenuItem('Approximate', self.on_ops)])
        ]

        self.menubar = MenuBar(menudropdowns)
        self.menubar.make(self.window)

        # TODO: dynamically twek width of rlong expressions
        self.expr_label = Label(self.window, text='', width=400)
        self.expr_label.grid(row=0, column=0)

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
        img = ImageTk.PhotoImage(Image.open(png_filename), master=self.window)
        self.expr_label.config(image=img)
        self.expr_label.photo = img

    def on_plot(self, a):

        if not isinstance(self.expr, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr)

    def on_python(self, a):

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

    def on_format(self, arg):

        formats = {'Canonical': 'canonical',
                   'Standard': 'standard',
                   'General': 'general',
                   'Time constant': 'timeconst',
                   'ZPK': 'ZPK',
                   'Partial fraction': 'partfrac',
                   'Time constant': 'timeconst'}

        method = formats[arg]

        e = ExprCalc(self.expr)
        expr = e.method(method)
        self.ui.show_expr_dialog(expr)

    def on_ops(self, arg):

        if arg == 'approximate':
            self.ui.show_approximate_dialog(self.expr)
        elif arg == 'simplify':
            self.ui.show_expr_dialog(self.expr.simplify())

    def on_transform(self, arg):

        domains = {'Time': 'time',
                   'Phasor': 'phasor',
                   'Laplace': 'laplace',
                   'Fourier': 'fourier',
                   'Frequency': 'frequency_response',
                   'Angular Fourier': 'angular_fourier',
                   'Angular Frequency': 'angular_frequency_response'}

        method = domains[arg]

        e = ExprCalc(self.expr)
        expr = e.method(method)
        self.ui.show_expr_dialog(expr)

    def on_edit(self, a):

        self.ui.show_message_dialog(self.expr)

    def on_latex(self, a):

        self.ui.show_message_dialog(self.expr.latex())
