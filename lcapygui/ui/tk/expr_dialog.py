from .menu import MenuDropdown, MenuItem
from .expr_calc import ExprCalc
from .exprimage import ExprImage
from lcapy import Expr, ExprTuple, Matrix, expr
from PIL import Image, ImageTk
from tkinter import Button, Label, Frame, BOTH, X
from .window import Window


def make_python(expr):
    """Return Python code that can be evaluated to create the
        expression."""

    # Output imports?

    symbols = expr.symbols

    s = ''
    for symbol in symbols:
        # Skip domain variables
        if symbol in ('f', 's', 't', 'w', 'omega',
                      'jf', 'jw', 'jomega', 'n', 'k', 'z'):
            continue

        # TODO, add other assumptions
        if symbols[symbol].is_positive:
            s += "%s = symbol('%s', positive=True)\n" % (symbol, symbol)
        else:
            s += "%s = symbol('%s')\n" % (symbol, symbol)

    s += repr(expr)
    return s


class ExprDialog(Window):

    def __init__(self, expr, ui, title=''):

        super(ExprDialog, self).__init__(ui, None, title)

        self.expr = expr
        self.titlestr = title

        mdd = None
        if isinstance(expr, Matrix):
            nrows = expr.rows
            ncols = expr.cols
            delim = '' if nrows < 10 else ','
            items = []
            for i in range(nrows):
                for j in range(ncols):
                    items.append(MenuItem('A%d%s%d' % (i + 1, delim, j + 1),
                                          self.on_element))

            mdd = MenuDropdown('Element', 0, items)

        menudropdowns = [
            MenuDropdown('File', 0,
                         [MenuItem('Save Python', self.on_save_python),
                          MenuItem('Save LaTeX', self.on_save_latex)
                          ]),
            MenuDropdown('Edit', 0,
                         [MenuItem('Expression', self.on_edit),
                          MenuItem('Python', self.on_edit_python)
                          ]),
            MenuDropdown('View', 0,
                         [MenuItem('Plot', self.on_plot),
                          MenuItem('LaTeX', self.on_latex),
                          MenuItem('Python', self.on_python),
                          MenuItem('Attributes', self.on_attributes)]),
            MenuDropdown('Manipulate', 0,
                         [MenuItem('Approximate', self.on_manipulate),
                          MenuItem('Evaluate', self.on_manipulate),
                          MenuItem('Limit', self.on_manipulate),
                          MenuItem('Parameterize', self.on_manipulate),
                          MenuItem('Poles', self.on_manipulate),
                          MenuDropdown('Simplify', 0,
                                       [MenuItem('Simplify', self.on_manipulate),
                                        MenuItem('Simplify conjugates',
                                                 self.on_manipulate),
                                        MenuItem('Simplify factors',
                                                 self.on_manipulate),
                                        MenuItem('Simplify terms',
                                                 self.on_manipulate),
                                        MenuItem('Simplify sin/cos',
                                                 self.on_manipulate),
                                        MenuItem('Simplify Dirac delta',
                                                 self.on_manipulate),
                                        MenuItem('Simplify Heaviside',
                                                 self.on_manipulate),
                                        MenuItem('Simplify rect',
                                                 self.on_manipulate),
                                        MenuItem('Rationalize denominator',
                                                 self.on_manipulate),
                                        MenuItem('Cancel terms',
                                                 self.on_manipulate),
                                        ]),
                          MenuItem('Solve', self.on_manipulate),
                          MenuItem('Substitute', self.on_manipulate),
                          MenuItem('Zeros', self.on_manipulate),
                          ]),
            MenuDropdown('Transform', 0,
                         [MenuItem('Time', self.on_transform),
                          MenuItem('Laplace', self.on_transform),
                          MenuItem('Phasor', self.on_transform),
                          MenuItem('Fourier', self.on_transform),
                          MenuItem('Angular Fourier', self.on_transform),
                          MenuItem('Frequency', self.on_transform),
                          MenuItem('Angular frequency', self.on_transform)]),
            MenuDropdown('Select', 0,
                         [mdd,
                          MenuItem('Real', self.on_select),
                          MenuItem('Imaginary', self.on_select),
                          MenuItem('Magnitude', self.on_select),
                          MenuItem('dB', self.on_select),
                          MenuItem('Sign', self.on_select),
                          MenuItem('Phase degrees', self.on_select),
                          MenuItem('Phase radians', self.on_select),
                          ]),
            MenuDropdown('Format', 0,
                         [MenuItem('Zero pole gain (ZPK)', self.on_format),
                          MenuItem('Canonical', self.on_format),
                          MenuItem('Time constant', self.on_format),
                          MenuItem('Time constant terms', self.on_format),
                          MenuItem('General', self.on_format),
                          MenuItem('Standard', self.on_format),
                          MenuItem('Partial fraction', self.on_format),
                          MenuItem('Polar', self.on_format),
                          MenuItem('Cartesian', self.on_format),
                          ]),
        ]

        self.add_menu(menudropdowns)

        png_filename = ExprImage(expr).image()
        image = Image.open(png_filename)

        self.expr_label = Label(self, text='', width=image.width + 100,
                                height=image.height + 100)
        self.expr_label.pack(fill=BOTH, expand=True)

        self.minsize(550, 100)
        self.focus()
        self.update()

    def update(self):

        try:
            self.show_img(self.expr)
        except Exception as e:
            self.expr_label.config(text=e)

    def show_img(self, e, pad=30):

        # TODO, fixme
        # if self.ui.model.preferences.show_units == 'true':
        #    e = e * e.units

        png_filename = ExprImage(e).image()

        image = Image.open(png_filename)

        right = pad
        left = pad
        top = pad
        bottom = pad

        width, height = image.size

        new_width = width + right + left
        new_height = height + top + bottom

        # Add border
        background = (245, 245, 245)
        image_pad = Image.new(image.mode, (new_width, new_height), background)
        image_pad.paste(image, (left, top))

        img_pad = ImageTk.PhotoImage(image_pad, master=self)

        self.expr_label.config(image=img_pad)
        self.expr_label.photo = img_pad

    def apply_attribute(self, attributes, arg):

        try:
            attribute = attributes[arg]

            e = ExprCalc(self.expr)
            expr = e.attribute(attribute)
            self.ui.show_expr_dialog(expr, title=self.titlestr)
        except Exception as e:
            self.ui.show_error_dialog(e)

    def apply_method(self, methods, arg):

        try:
            method = methods[arg]

            e = ExprCalc(self.expr)
            expr = e.method(method)
            self.ui.show_expr_dialog(expr, title=self.titlestr)
        except Exception as e:
            self.ui.show_error_dialog(e)

    def on_attributes(self, arg):

        self.ui.show_expr_attributes_dialog(self.expr, title=self.titlestr)

    def on_edit(self, arg):

        self.ui.show_edit_dialog(self.expr)

    def on_edit_python(self, arg):

        self.ui.show_python_dialog(self.expr)

    def on_format(self, arg):

        formats = {'Canonical': 'canonical',
                   'Standard': 'standard',
                   'General': 'general',
                   'Time constant': 'timeconst',
                   'Time constant terms': 'timeconst_terms',
                   'Zero pole gain (ZPK)': 'ZPK',
                   'Partial fraction': 'partfrac',
                   'Time constant': 'timeconst',
                   'Polar': 'polar',
                   'Cartesian': 'cartesian'}

        if arg in ('Polar', 'Cartesian'):
            # What was I thinking?
            self.apply_attribute(formats, arg)
        else:
            self.apply_method(formats, arg)

    def on_latex(self, arg):

        self.ui.show_message_dialog(self.expr.latex())

    def on_manipulate(self, arg):

        simplify = {'Simplify': 'simplify',
                    'Simplify conjugates': 'simplify_conjugates',
                    'Simplify factors': 'simplify_factors',
                    'Simplify terms': 'simplify_terms',
                    'Simplify sin/cos': 'simplify_sin_cos',
                    'Simplify Dirac delta': 'simplify_dirac_delta',
                    'Simplify Heaviside': 'simplify_heaviside',
                    'Simplify rect': 'simplify_rect',
                    'Cancel terms': 'cancel_terms',
                    'Rationalize denominator': 'rationalize_denominator'}

        try:
            if arg == 'Approximate':
                self.ui.show_approximate_dialog(self.expr, title=self.titlestr)
            elif arg == 'Evaluate':
                self.ui.show_expr_dialog(
                    expr(self.expr.evaluate()), title=self.titlestr)
            elif arg == 'Limit':
                self.ui.show_limit_dialog(self.expr, title=self.titlestr)
            elif arg == 'Parameterize':
                self.ui.show_expr_dialog(ExprTuple(self.expr.parameterize()),
                                         title=self.titlestr)
            elif arg == 'Poles':
                self.ui.show_expr_dialog(
                    self.expr.poles(), title=self.titlestr)
            elif arg in simplify:
                self.apply_method(simplify, arg)
            elif arg == 'Solve':
                self.ui.show_expr_dialog(
                    self.expr.solve(), title=self.titlestr)
            elif arg == 'Substitute':
                self.ui.show_subs_dialog(self.expr, title=self.titlestr)
            elif arg == 'Zeros':
                self.ui.show_expr_dialog(
                    self.expr.zeros(), title=self.titlestr)
        except Exception as e:
            self.ui.show_error_dialog(e)

    def on_save_latex(self, arg):

        pathname = self.ui.save_file_dialog('expr.tex', doc='LaTeX file',
                                            ext='*.tex')
        if pathname == '' or pathname == ():
            return

        with open(pathname, 'w') as f:
            f.write(self.expr.latex())

    def on_save_python(self, arg):

        pathname = self.ui.save_file_dialog('expr.py', doc='Python file',
                                            ext='*.py')
        if pathname == '' or pathname == ():
            return

        with open(pathname, 'w') as f:
            f.write(make_python(self.expr))

    def on_select(self, arg):

        parts = {'Real': 'real',
                 'Imaginary': 'imag',
                 'Magnitude': 'magnitude',
                 'dB': 'dB',
                 'Sign': 'sign',
                 'Phase degrees': 'phase_degrees',
                 'Phase radian': 'phase_radians'}

        self.apply_attribute(parts, arg)

    def on_element(self, arg):

        arg = arg[1:]

        if ',' in arg:
            r, c = arg.split(',')
        else:
            r = arg[0]
            c = arg[1]

        row = int(r) - 1
        col = int(c) - 1

        e = ExprCalc(self.expr)
        expr = e.eval('[%s, %d]' % (row, col))
        self.ui.show_expr_dialog(expr, title=self.titlestr)

    def on_plot(self, arg):

        if not isinstance(self.expr, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr)

    def on_python(self, arg):

        s = make_python(self.expr)

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
