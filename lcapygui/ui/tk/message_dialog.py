from tkinter import Tk, Text, END


class MessageDialog:

    def __init__(self, message, title=''):

        self.window = Tk()
        self.window.title(title)

        text = Text(self.window)
        text.pack()

        text.insert(END, message)
