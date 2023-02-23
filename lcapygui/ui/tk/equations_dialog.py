from tkinter import Tk
from tkinter.ttk import Button, Label
from PIL import Image, ImageTk

from .lateximage import LatexImage


# See https://stackoverflow.com/questions/56043767/
# show-large-image-using-scrollbar-in-python

class EquationsDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.ui = ui
        self.labelentries = None
        self.title = title

        s = '\\begin{tabular}{ll}\n'

        for k, v in expr.items():
            if not isinstance(k, str):
                k = k.latex()

            s += '$' + k + '$: & $' + v.latex() + '$\\\\ \n'

        s += '\\end{tabular}\n'
        self.s = s

        self.master = Tk()
        self.master.title(title)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=0)

        button = Button(self.master, text="LaTeX", command=self.on_latex)
        button.grid(row=1, sticky='w')

        self.update()

    def update(self):

        try:
            self.show_img()
        except Exception as e:
            self.expr_label.config(text=e)

    def show_img(self):

        png_filename = LatexImage(self.s).image()
        img = ImageTk.PhotoImage(Image.open(png_filename), master=self.master)
        self.expr_label.config(image=img)
        self.expr_label.photo = img

    def on_latex(self):

        self.ui.show_message_dialog(self.s)
