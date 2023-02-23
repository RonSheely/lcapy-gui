from tkinter import Tk
from tkinter.ttk import Button, Label
from PIL import Image, ImageTk
from lcapy import Expr
from .labelentries import LabelEntry, LabelEntries
from .exprimage import ExprImage


global_dict = {}
exec('from lcapy import *', global_dict)


class ExprAdvancedDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.expr_tweak = expr
        self.ui = ui
        self.labelentries = None

        self.operation = 'result'

        self.format = ''

        self.formats = {'': '',
                        'Canonical': 'canonical',
                        'Standard': 'standard',
                        'ZPK': 'ZPK',
                        'Partial fraction': 'partfrac',
                        'Time constant': 'timeconst'}

        self.domain = ''

        self.domains = {'': '',
                        'Time': 'time',
                        'Phasor': 'phasor',
                        'Laplace': 'laplace',
                        'Fourier': 'fourier',
                        'Frequency': 'frequency_response',
                        'Angular Fourier': 'angular_fourier',
                        'Angular Frequency': 'angular_frequency_response'}

        self.master = Tk()
        self.master.title(title)

        entries = [LabelEntry('operation', 'Operation', self.operation,
                              None, self.on_operation),
                   LabelEntry('domain', 'Domain', self.domain,
                              list(self.domains.keys()), self.on_domain),
                   LabelEntry('format', 'Format', self.format,
                              list(self.formats.keys()), self.on_format)]

        self.labelentries = LabelEntries(self.master, ui, entries)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=self.labelentries.row, columnspan=4)

        button = Button(self.master, text="Plot", command=self.on_plot)
        button.grid(row=self.labelentries.row + 1, sticky='w')

        button = Button(self.master, text="LaTeX", command=self.on_latex)
        button.grid(row=self.labelentries.row + 1, column=1, sticky='w')

        self.update()

    def on_format(self, format):

        if format == self.format:
            return
        self.format = format
        self.update()

    def on_domain(self, domain):

        if domain == self.domain:
            return
        self.domain = domain
        self.update()

    def on_operation(self, *args):

        self.operation = self.labelentries.get_text('operation')
        self.update()

    def update(self):

        operation = self.operation
        format = self.format
        domain = self.domain

        command = '(' + operation + ')'
        if domain != '':
            command += '.' + self.domains[domain] + '()'
        if format != '':
            command += '.' + self.formats[format] + '()'

        if self.ui.debug:
            print('Expression command: ' + command)
            print(self.expr)

        global_dict['result'] = self.expr
        try:
            # Perhaps evaluate domain and transform steps
            # separately if operation is not an Lcapy Expr?
            self.expr_tweak = eval(command, global_dict)
            # self.show_pretty(e)
            self.show_img(self.expr_tweak)
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

        if not isinstance(self.expr_tweak, Expr):
            self.ui.info_dialog('Cannot plot expression')
            return

        self.ui.show_plot_properties_dialog(self.expr_tweak)

    def on_latex(self):

        self.ui.show_message_dialog(self.expr_tweak.latex())
