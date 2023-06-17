from tkinter import Menu


class MenuItem:

    def __init__(self, label, command, underline=0, accelerator=None):

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

        # Create the drop down menus
        self.menubar = Menu(window, bg='lightgrey', fg='black')

        self.menus = []

        for menudropdown in self.menudropdowns:
            menu = Menu(self.menubar, tearoff=0,
                        bg='lightgrey', fg='black')

            for menuitem in menudropdown.menuitems:
                menu.add_command(label=menuitem.label,
                                 command=lambda a=menuitem.label: menuitem.command(
                                     a),
                                 underline=menuitem.underline,
                                 accelerator=menuitem.accelerator)

            self.menubar.add_cascade(label=menudropdown.label,
                                     underline=menudropdown.underline,
                                     menu=menu)
            self.menus.append(menu)

        window.config(menu=self.menubar)
