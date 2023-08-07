from tkinter import Button, Label, Frame, BOTH, X
from PIL import Image, ImageTk
from .window import Window


class ImageDialog(Window):

    def __init__(self, ui, filename, title=''):

        super().__init__(ui, None, title)

        image = Image.open(filename)

        width, height = image.size

        label = Label(self, text='', width=image.width,
                      height=image.height)
        label.pack(fill=BOTH, expand=True)

        img = ImageTk.PhotoImage(image, master=self)

        label.config(image=img)
        label.photo = img
