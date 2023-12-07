from lcapygui import node
from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from astar import AStar
import random


class UIModelDnD(UIModelMPH):

    """
    UIModelDnD

    Attributes
    ==========
    chain_path : lcapy.mnacpts.Cpt or None
        The component to be placed after a key is pressed

    """

    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)
        self.chain_path = []

    def on_add_cpt(self, thing):
        """
        Adds a component to the circuit after a key is pressed

        Explanation
        ===========
        If there are cursors present, it will place a component between them
        otherwise, the component will be placed

        Parameters
        ==========
        thing : lcapygui.ui.uimodelbase.C or None
            The key pressed

        """

        if self.ui.debug:
            print(f"adding {thing.cpt_type} to mouse position: {self.mouse_position}")

        # Get mouse positions
        mouse_x = self.mouse_position[0]
        mouse_y = self.mouse_position[1]

        if len(self.cursors) < 2:
            x1, y1 = self.snap_to_grid(mouse_x, mouse_y)
            if len(self.cursors) == 1:
                x1 = self.cursors[0].x
                y1 = self.cursors[0].y
                self.cursors.remove()

            cpt = self.cpt_create("DW", x1, y1, mouse_x, mouse_y)

            cpt.gcpt.convert_to_wires(self)
            self.on_redraw()
        else:
            # add the component like normal
            if thing.cpt_type == "W":
                thing.cpt_type = "DW"
            super().on_add_cpt(thing)

    def on_mouse_release(self):
        super().on_mouse_release()

        # IF a node was moved, update history
        if self.selected and not self.cpt_selected:
            self.on_redraw()

    def on_left_double_click(self, x, y):
        self.on_select(x, y)
        if self.cpt_selected and self.selected.gcpt.type == "DW":
            self.history.append(HistoryEvent("D", self.selected))
            self.selected.gcpt.convert_to_wires(self)
        else:
            super().on_left_double_click(x, y)

    def on_mouse_drag(self, mouse_x, mouse_y, key):
        """
        Performs operations on mouse drag

        Explanation
        -----------
        This function is called when the user drags the mouse on the canvas.

        Parameters
        ----------
        mouse_x: float
            x position of the mouse
        mouse_y : float
            y position of the mouse
        key : str
            String representation of the pressed key.

        Returns
        -------

        """

        if self.selected and not self.cpt_selected:
            new_x, new_y = self.snap_to_grid(mouse_x, mouse_y)

            self.selected.pos.x = new_x
            self.selected.pos.y = new_y

            for cpt in self.selected.connected:
                cpt.gcpt.undraw()
                cpt.gcpt.draw(self)

                self.ui.refresh()
        else:
            super().on_mouse_drag(mouse_x, mouse_y, key)