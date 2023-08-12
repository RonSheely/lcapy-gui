from tkinter import END
from tkinter.scrolledtext import ScrolledText
from .window import Window


class MessageDialog(Window):

    def __init__(self, message, title=''):

        super().__init__(None, None, title)

        text = ScrolledText(self)
        text.pack()

        text.insert(END, message)
