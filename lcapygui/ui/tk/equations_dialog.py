from tkinter import Tk,  Label
from PIL import Image, ImageTk

from .expr_image import ExprImage


global_dict = {}
exec('from lcapy import *', global_dict)


class EquationsDialog:

    def __init__(self, expr, ui, title=''):

        self.expr = expr
        self.ui = ui
        self.labelentries = None
        self.title = title

        self.master = Tk()
        self.master.title(title)

        self.expr_label = Label(self.master, text='')
        self.expr_label.grid(row=0, columnspan=4)

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
