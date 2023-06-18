from tkinter import Tk, Button, Label
from PIL import Image, ImageTk

from lcapy import Expr, ExprTuple
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
                          MenuItem('Python', self.on_python),
                          MenuItem('Attributes', self.on_attributes)]),
            MenuDropdown('Edit', 0,
                         [MenuItem('Expression', self.on_edit)]),
            MenuDropdown('Part', 0,
                         [MenuItem('Real', self.on_part),
                          MenuItem('Imaginary', self.on_part),
                          MenuItem('Magnitude', self.on_part),
                          MenuItem('Phase degrees', self.on_part),
                          MenuItem('Phase radians', self.on_part),
                          ]),
            MenuDropdown('Format', 0,
                         [MenuItem('ZPK', self.on_format),
                          MenuItem('Canonical', self.on_format),
                          MenuItem('Time constant', self.on_format),
                          MenuItem('Time constant terms', self.on_format),
                          MenuItem('General', self.on_format),
                          MenuItem('Standard', self.on_format),
                          MenuItem('Partial fraction', self.on_format)]),
            MenuDropdown('Transform', 0,
                         [MenuItem('Time', self.on_transform),
                          MenuItem('Laplace', self.on_transform),
                          MenuItem('Phasor', self.on_transform),
                          MenuItem('Fourier', self.on_transform),
                          MenuItem('Angular Fourier', self.on_transform),
                          MenuItem('Frequency', self.on_transform),
                          MenuItem('Angular frequency', self.on_transform)]),
            MenuDropdown('Operations', 0,
                         [MenuItem('Approximate', self.on_operations),
                          MenuItem('Evaluate', self.on_operations),
                          MenuItem('Parameterize', self.on_operations),
                          MenuItem('Poles', self.on_operations),
                          MenuDropdown('Simplify', 0,
                                       [MenuItem('Simplify', self.on_operations),
                                        MenuItem('Simplify conjugates',
                                                 self.on_operations),
                                        MenuItem('Simplify factors',
                                                 self.on_operations),
                                        MenuItem('Simplify terms',
                                                 self.on_operations),
                                        MenuItem('Simplify sin/cos',
                                                 self.on_operations),
                                        MenuItem('Simplify Dirac delta',
                                                 self.on_operations),
                                        MenuItem('Simplify Heaviside',
                                                 self.on_operations),
                                        MenuItem('Simplify rect',
                                                 self.on_operations),
                                        ]),
                          MenuItem('Solve', self.on_operations),
                          MenuItem('Subs', self.on_operations),
                          MenuItem('Zeros', self.on_operations),
                          ])
        ]

        self.menubar = MenuBar(menudropdowns)
        self.menubar.make(self.window)

        # TODO: dynamically tweak width of long expressions
        self.expr_label = Label(self.window, text='')
        self.expr_label.pack(fill='x')

        #self.expr_label.place(anchor="c", relx=.50, rely=.50)

        self.window.minsize(500, 100)

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

    def apply_attribute(self, attributes, arg):

        attribute = attributes[arg]

        e = ExprCalc(self.expr)
        expr = e.attribute(attribute)
        self.ui.show_expr_dialog(expr, title=self.title)

    def apply_method(self, methods, arg):

        method = methods[arg]

        e = ExprCalc(self.expr)
        expr = e.method(method)
        self.ui.show_expr_dialog(expr, title=self.title)

    def on_attributes(self, arg):

        self.ui.show_expr_attributes_dialog(self.expr, title=self.title)

    def on_edit(self, arg):

        self.ui.show_edit_dialog(self.expr)

    def on_format(self, arg):

        formats = {'Canonical': 'canonical',
                   'Standard': 'standard',
                   'General': 'general',
                   'Time constant': 'timeconst',
                   'Time constant terms': 'timeconst_terms',
                   'ZPK': 'ZPK',
                   'Partial fraction': 'partfrac',
                   'Time constant': 'timeconst'}

        self.apply_method(formats, arg)

    def on_latex(self, arg):

        self.ui.show_message_dialog(self.expr.latex())

    def on_operations(self, arg):

        try:
            if arg == 'Approximate':
                self.ui.show_approximate_dialog(self.expr, title=self.title)
            elif arg == 'Evaluate':
                self.ui.show_approximate_dialog(
                    self.expr.evaluate(), title=self.title)
            elif arg == 'Parameterize':
                self.ui.show_expr_dialog(ExprTuple(self.expr.parameterize()),
                                         title=self.title)
            elif arg == 'Poles':
                self.ui.show_expr_dialog(
                    self.expr.poles(), title=self.title)
            elif arg == 'Simplify':
                methods = {'Simplify': 'simplify',
                           'Simplify conjugates': 'simplify_conjugates',
                           'Simplify factors': 'simplify_factors',
                           'Simplify terms': 'simplify_terms',
                           'Simplify sin/cos': 'simplify_sin_cos',
                           'Simplify Dirac delta': 'simplify_dirac_delta',
                           'Simplify Heaviside': 'simplify_heaviside',
                           'Simplify rect': 'simplify_rect'}
                self.apply_method(methods, arg)
            elif arg == 'Solve':
                self.ui.show_expr_dialog(
                    self.expr.solve(), title=self.title)
            elif arg == 'Subs':
                self.ui.show_subs_dialog(self.expr, title=self.title)
            elif arg == 'Zeros':
                self.ui.show_expr_dialog(
                    self.expr.zeros(), title=self.title)
        except Exception as e:
            self.ui.show_error_dialog(e)

    def on_part(self, arg):

        parts = {'Real': 'real',
                 'Imaginary': 'imag',
                 'Magnitude': 'magnitude',
                 'Phase degrees': 'phase_degrees',
                 'Phase radian': 'phase_radians'}

        self.apply_attribute(parts, arg)

    def on_plot(self, arg):

        if not isinstance(self.expr, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr)

    def on_python(self, arg):

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

    def on_transform(self, arg):

        domains = {'Time': 'time',
                   'Phasor': 'phasor',
                   'Laplace': 'laplace',
                   'Fourier': 'fourier',
                   'Frequency': 'frequency_response',
                   'Angular Fourier': 'angular_fourier',
                   'Angular frequency': 'angular_frequency_response'}

        self.apply_method(domains, arg)
