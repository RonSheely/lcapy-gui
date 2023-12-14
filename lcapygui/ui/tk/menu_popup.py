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
                        )

            elif isinstance(menuitem, MenuSeparator):
                self.menu.add_separator()
            else:
                self.menu.add_command(
                    label=menuitem.label,
                    command=lambda a=menuitem: doit(a),
                    underline=menuitem.underline,
                    accelerator=menuitem.accelerator,
                )

    def do_popup(self, x, y):
        try:
            self.menu.tk_popup(x, y)
        finally:
            self.menu.grab_release()

    def undo_popup(self):
        self.menu.unpost()


def make_popup(ui, menu_items):
    MenuTable = {
        "Copy": MenuItem("Copy", ui.on_copy, accelerator="Ctrl+c"),
        "Cut": MenuItem("Cut", ui.on_cut, accelerator="Ctrl+x"),
        "Inspect": MenuDropdown(
                    "Inspect",
                    0,
                    [
                        MenuItem("Voltage", ui.on_inspect_voltage),
                        MenuItem("Current", ui.on_inspect_current),
                        MenuItem(
                            "Thevenin impedance", ui.on_inspect_thevenin_impedance
                        ),
                        MenuItem("Norton admittance", ui.on_inspect_norton_admittance),
                        MenuItem("Noise voltage", ui.on_inspect_noise_voltage),
                        MenuItem("Noise current", ui.on_inspect_noise_current),
                    ],
                ),
    }
    display_items = []
    for menu_item in menu_items:
        if menu_item not in MenuTable:
            raise ValueError("Menu item not found")
        else:
            display_items.append(MenuTable[menu_item])

    ui.popup_menu = MenuPopup(
        MenuDropdown(
            "Right click",
            0,
            display_items,
        )
    )
    ui.popup_menu.make(ui, ui.level)
    ui.popup_menu.do_popup(ui.canvas.winfo_pointerx(), ui.canvas.winfo_pointery())


def unmake_popup(ui):
    if ui.popup_menu is not None:
        ui.popup_menu.undo_popup()
        ui.popup_menu = None
