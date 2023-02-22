from tkinter import Tk
from tkinter.ttk import Label
from PIL import Image, ImageTk

from .expr_image import ExprImage


# See https://stackoverflow.com/questions/56043767/
# show-large-image-using-scrollbar-in-python

class EquationsDialog:

    def __init__(self, expr, ui, title=''):

        if isinstance(expr, dict):

        self.expr = expr
        self.ui = ui
        self.labelentries = None
        self.title = title

        self.master = Tk()
        self.master.title(title)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=0)

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
