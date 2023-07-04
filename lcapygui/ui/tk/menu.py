from tkinter import Menu


class MenuItem:

    def __init__(self, label, command=None, underline=0, accelerator=None):

        self.label = label
        self.command = command
        self.underline = underline
        self.accelerator = accelerator


class MenuDropdown:

    def __init__(self, label, underline=0, menuitems=None):

        self.label = label
        self.underline = underline
        self.menuitems = menuitems


class MenuBar:

    def __init__(self, menudropdowns):

        self.menudropdowns = menudropdowns

    def make(self, window):

        def doit(menuitem):

            menuitem.command(menuitem.label)

        # Create the drop down menus
        self.menubar = Menu(window, bg='lightgrey', fg='black')

        self.menus = []

        for menudropdown in self.menudropdowns:
            menu = Menu(self.menubar, tearoff=0, bg='lightgrey', fg='black')

            self.menubar.add_cascade(label=menudropdown.label,
                                     underline=menudropdown.underline,
                                     menu=menu)

            for menuitem in menudropdown.menuitems:

                if menuitem is None:
                    continue

                if isinstance(menuitem, MenuDropdown):

                    submenu = Menu(self.menubar, tearoff=0,
                                   bg='lightgrey', fg='black')
                    menu.add_cascade(label=menuitem.label,
                                     underline=menuitem.underline,
                                     menu=submenu)
                    for submenuitem in menuitem.menuitems:
                        submenu.add_command(label=submenuitem.label,
                                            command=lambda a=submenuitem: doit(
                                                a),
                                            underline=submenuitem.underline,
                                            accelerator=submenuitem.accelerator)

                else:
                    menu.add_command(label=menuitem.label,
                                     command=lambda a=menuitem: doit(a),
                                     underline=menuitem.underline,
                                     accelerator=menuitem.accelerator)

            self.menus.append(menu)

        window.config(menu=self.menubar)
