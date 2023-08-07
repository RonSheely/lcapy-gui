from tkinter import Toplevel
from .menu import MenuBar


class Window(Toplevel):

    def __init__(self, ui, name, title):

        super(Window, self).__init__()

        self.ui = ui
        self.name = name
        self.title(title)

        if ui is not None:
            self.report_callback_exception = ui.report_callback_exception

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.debug = False

    def add_menu(self, menudropdowns):

        self.menubar = MenuBar(menudropdowns)
        self.menubar.make(self)

    def focus(self):

        if self.debug:
            print('focus')

        super(Window, self).focus()

        # Put window on top
        self.attributes('-topmost', True)

    def on_close(self):

        if self.debug:
            print('on close')

        self.destroy()
        if self.ui is not None:
            self.ui.dialogs.pop(self.name, None)
