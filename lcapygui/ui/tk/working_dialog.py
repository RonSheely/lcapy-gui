from tkinter import Tk
from tkinter.messagebox import showinfo


class WorkingDialog:

    def __init__(self, message, title=''):

        if False:
            # Need to make this non-modal
            self.window = Tk()
            self.window.title(title)

            showinfo('', message)

        # Marvellous if could display warning messages here...

    def destroy(self):

        if False:
            self.window.destroy()
