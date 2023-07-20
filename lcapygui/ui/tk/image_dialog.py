from tkinter import Tk, Button, Label, Frame, BOTH, X
from PIL import Image, ImageTk


class ImageDialog(Tk):

    def __init__(self, ui, filename, title=''):

        super().__init__()

        self.report_callback_exception = ui.report_callback_exception
        self.title(title)

        image = Image.open(filename)

        pad = 30
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

        expr_label = Label(self, text='', width=image.width + 100,
                           height=image.height + 100)
        expr_label.pack(fill=BOTH, expand=True)

        img_pad = ImageTk.PhotoImage(image_pad, master=self)

        expr_label.config(image=img_pad)
        expr_label.photo = img_pad
