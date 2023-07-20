from tkinter import Tk, Button, Label, Frame, BOTH, X
from PIL import Image, ImageTk


class ImageDialog(Tk):

    def __init__(self, ui, filename, title=''):

        super().__init__()

        self.report_callback_exception = ui.report_callback_exception
        self.title(title)

        image = Image.open(filename)

        width, height = image.size

        label = Label(self, text='', width=image.width,
                      height=image.height)
        label.pack(fill=BOTH, expand=True)

        img = ImageTk.PhotoImage(image, master=self)

        label.config(image=img)
        label.photo = img
