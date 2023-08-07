from tkinter.ttk import Button, Label
from PIL import Image, ImageTk

from .lateximage import LatexImage
from .window import Window


# See https://stackoverflow.com/questions/56043767/
# show-large-image-using-scrollbar-in-python

class EquationsDialog(Window):

    def __init__(self, expr, ui, title=''):

        super().__init__(ui, None, title)

        self.expr = expr
        self.labelentries = None

        s = '\\begin{tabular}{ll}\n'

        for k, v in expr.items():
            if not isinstance(k, str):
                k = k.latex()

            s += '$' + k + '$: & $' + v.latex() + '$\\\\ \n'

        s += '\\end{tabular}\n'
        self.s = s

        self.expr_label = Label(self, text='')
        self.expr_label.grid(row=0)

        button = Button(self, text="LaTeX", command=self.on_latex)
        button.grid(row=1, sticky='w')

        self.update()

    def update(self):

        try:
            self.show_img()
        except Exception as e:
            self.expr_label.config(text=e)

    def show_img(self):

        png_filename = LatexImage(self.s).image()
        img = ImageTk.PhotoImage(Image.open(png_filename), master=self)
        self.expr_label.config(image=img)
        self.expr_label.photo = img

    def on_latex(self):

        self.ui.show_message_dialog(self.s)
