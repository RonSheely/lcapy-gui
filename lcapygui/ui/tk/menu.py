from tkinter import Menu


class MenuSeparator:
    level = 0


class MenuItem:
    def __init__(
        self, label, command=None, arg=None, underline=0, accelerator=None, level=0, state="normal"
    ):
        self.label = label
        self.command = command
        self.arg = arg
        self.underline = underline
        self.accelerator = accelerator
        self.level = level
        self.state = state


class MenuDropdown:
    def __init__(self, label, underline=0, menuitems=None, level=0):
        self.label = label
        self.underline = underline
        self.menuitems = menuitems
        self.level = level


class MenuBar:
    def __init__(self, menudropdowns):
        self.menudropdowns = menudropdowns

    def make(self, window, level=10):
        def doit(menuitem):
            arg = menuitem.arg
            if arg is None:
                arg = menuitem.label

            menuitem.command(arg)

        # Create the drop down menus
        self.menubar = Menu(window, bg="lightgrey", fg="black")

        self.menus = []

        for menudropdown in self.menudropdowns:
            menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")

            self.menubar.add_cascade(
                label=menudropdown.label, underline=menudropdown.underline, menu=menu
            )

            for menuitem in menudropdown.menuitems:
                if menuitem is None:
                    continue
                if menuitem.level > level:
                    continue

                if isinstance(menuitem, MenuDropdown):
                    submenu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
                    menu.add_cascade(
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
                                state=submenuitem.state
                            )

                elif isinstance(menuitem, MenuSeparator):
                    menu.add_separator()
                else:
                    menu.add_command(
                        label=menuitem.label,
                        command=lambda a=menuitem: doit(a),
                        underline=menuitem.underline,
                        accelerator=menuitem.accelerator,
                        state = menuitem.state
                    )

            self.menus.append(menu)

        window.config(menu=self.menubar)
