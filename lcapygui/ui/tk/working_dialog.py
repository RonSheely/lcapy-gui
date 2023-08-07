from tkinter.messagebox import showinfo
from .window import Window


class WorkingDialog(Window):

    def __init__(self, message, title=''):

        if False:
            # Need to make this non-modal
            super().__init__(None, None, title)

            showinfo('', message)

        # Marvellous if could display warning messages here...

    def destroy(self):

        if False:
            self.on_close()
