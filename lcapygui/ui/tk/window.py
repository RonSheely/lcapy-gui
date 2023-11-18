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

    def add_menu(self, menudropdowns, level=10):

        self.menubar = MenuBar(menudropdowns)
        self.menubar.make(self, level)

    def focus(self):

        if self.debug:
            print('focus')

        super(Window, self).focus()

        # Put window on top, however, this makes it stay above all others
        self.attributes('-topmost', True)
        # Don't force the window to stay on top.  The user can force
        # the window to stay on top if they wish.
        self.attributes('-topmost', False)

        # self.lift()

    def topmost(self):
        """ Put window on top, however, this makes it stay above all others."""

        self.attributes('-topmost', True)

    def on_close(self):

        if self.debug:
            print('on close')

        self.destroy()
        if self.ui is not None:
            self.ui.dialogs.pop(self.name, None)
