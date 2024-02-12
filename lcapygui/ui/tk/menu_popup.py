from .menu import MenuItem, MenuDropdown, MenuSeparator
from tkinter import Menu


class MenuPopup:
    def __init__(self, menu_dropdown):
        self.menu_dropdown = menu_dropdown
        self.menu = None

    def make(self, window, level=10):
        def doit(menuitem):
            arg = menuitem.arg
            if arg is None:
                arg = menuitem.label

            menuitem.command(arg)

        self.menu = Menu(window, tearoff=0)

        for menuitem in self.menu_dropdown.menuitems:
            if menuitem is None:
                continue
            if menuitem.level > level:
                continue

            if isinstance(menuitem, MenuDropdown):
                submenu = Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
                self.menu.add_cascade(
                    label=menuitem.label, underline=menuitem.underline, menu=submenu
                )
                for submenuitem in menuitem.menuitems:
                    if isinstance(submenuitem, MenuSeparator):
                        submenu.add_separator()
                    else:
                        submenu.add_command(
                            label=submenuitem.label,
                            command=lambda a=submenuitem: doit(a),
                            underline=submenuitem.underline,
                            accelerator=submenuitem.accelerator,
                            state = menuitem.state
                        )

            elif isinstance(menuitem, MenuSeparator):
                self.menu.add_separator()
            else:
                self.menu.add_command(
                    label=menuitem.label,
                    command=lambda a=menuitem: doit(a),
                    underline=menuitem.underline,
                    accelerator=menuitem.accelerator,
                    state=menuitem.state
                )

    def do_popup(self, x, y):
        try:
            self.menu.tk_popup(x, y)
        finally:
            self.menu.grab_release()

    def undo_popup(self):
        self.menu.unpost()
