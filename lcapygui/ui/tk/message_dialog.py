from tkinter import Text, END
from .window import Window


class MessageDialog(Window):

    def __init__(self, message, title=''):

        super().__init__(None, None, title)

        text = Text(self)
        text.pack()

        text.insert(END, message)
