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

        if len(self.cursors) < 102:
            x1, y1 = self.snap_to_grid(mouse_x, mouse_y)
            if len(self.cursors) == 1:
                x1 = self.cursors[0].x
                y1 = self.cursors[0].y
                self.cursors.remove()

            self.cpt_create("W", x1, y1, mouse_x, mouse_y)
            self.on_redraw()

        else:
            # add the component like normal
            super().on_add_cpt(thing)

    def on_mouse_move(self, mouse_x, mouse_y):
        """
        Performs operations on mouse movement

        Explanation
        -----------
        This function is called when the user moves the mouse on the canvas.
        If a component is being placed, it will follow the mouse.

        Parameters
        ----------
        mouse_x : float
            x position of the mouse
        mouse_y : float
            y position of the mouse

        """
        if self.chain_path != []:
            # Get start node
            cpt = self.chain_path[0]
            x1 = cpt.nodes[0].pos.x
            x2 = cpt.nodes[0].pos.y
            type = cpt.type

            self.draw_path("W", x1, x2, mouse_x, mouse_y)

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
            print(f"moving node to {new_x}, {new_y}")
            self.selected.pos.x = new_x
            self.selected.pos.y = new_y
            self.on_redraw()
        else:
            super().on_mouse_drag(mouse_x, mouse_y, key)
