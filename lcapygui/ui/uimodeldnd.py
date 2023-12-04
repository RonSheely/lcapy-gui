from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH


class UIModelDnD(UIModelMPH):

    """
    UIModelDnD

    Attributes
    ==========
    chain_place : lcapy.mnacpts.Cpt or None
        The component to be placed after a key is pressed
    """
    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)
        self.chain_place = None

    def on_add_cpt(self, thing):
        """
        Adds a component to the circuit after a key is pressed

        Explanation
        ===========
        If there are cursors present, it will place a component between them
        otherwise, the component will be placed

        Parameters
        ==========
        thing : ui.uimodelbase.C
            The key pressed


        """

        if self.ui.debug:
            print(f"adding {thing.cpt_type} to mouse position: {self.mouse_position}")

        # Get mouse positions
        mouse_x = self.mouse_position[0]
        mouse_y = self.mouse_position[1]

        if len(self.cursors) < 2 and self.chain_place is None:
            x1, y1 = self.snap_to_grid(mouse_x, mouse_y)
            if len(self.cursors) == 1:
                x1 = self.cursors[0].x
                y1 = self.cursors[0].y
                self.cursors.remove()

            self.chain_place = self.thing_create(thing.cpt_type, x1, y1, mouse_x, mouse_y)
            self.ui.refresh()

        else:
            # add a new cursor at the grid position closest to the mouse
            self.add_cursor(round(mouse_x), round(mouse_y))

            # add the component like normal
            super().on_add_cpt(thing)

    def on_left_click(self, mouse_x, mouse_y):
        """
        Performs operations on left-click

        Explanation
        ===========
        This function is called when the user left-clicks on the canvas.
        If a component is currently being dragged, it will drop the component
        Otherwise, it selects the component at the mouse position

        Parameters
        ==========
        :param float mouse_x: x position of the mouse
        :param float mouse_y: y position of the mouse

        """

        self.on_select(mouse_x, mouse_y)

        # If placing a component without cursors
        if self.chain_place is not None:
            cpt = self.chain_place
            self.cursors.remove()

            x1, y1 = cpt.gcpt.node2.pos.x, cpt.gcpt.node2.pos.y
            x2, y2 = mouse_x, mouse_y

            if cpt.type == "W":
                self.chain_place = self.thing_create(self.chain_place.type, x1, y1, x2, y2)
            else:
                self.chain_place = None
        else:
            if self.ui.debug:
                print("Add node at (%s, %s)" % (mouse_x, mouse_y))
            #self.cursors.remove()  # TODO: stop clearing nodes on click when node-dragging is implemented
            #self.on_add_node(mouse_x, mouse_y)
            super().on_left_click(mouse_x, mouse_y)

    def on_right_click(self, x, y):
        """
        performs operations on right-click

        Explanation
        ===========
        This function is called when the user right-clicks on the canvas.
        If no component is selected, it will clear the cursors from the screen.
        Otherwise, it will show the selected components properties dialogue

        Parameters
        ==========
        x : float
            x position of the mouse
        y : float
            y position of the mouse

        """
        if self.chain_place is not None:
            print("Chain create disabled. Deleting  " + self.chain_place.name)
            self.cpt_delete(self.chain_place)
            self.chain_place = None

        else:
            super().on_right_click(x, y)
        self.unselect()

    def on_mouse_move(self, mouse_x, mouse_y):
        if self.chain_place != None:
            cpt = self.chain_place
            new_x, new_y = self.snap_to_grid(mouse_x, mouse_y)
            if self.ui.debug:
                print(f"moving node to {new_x}, {new_y}")
            cpt.nodes[1].pos.x = new_x
            cpt.nodes[1].pos.y = new_y
            self.on_redraw()

    def on_mouse_drag(self, x, y, key):

        if self.selected and not self.cpt_selected:

            new_x, new_y = self.snap_to_grid(x, y)
            print(f"moving node to {new_x}, {new_y}")
            self.selected.pos.x = new_x
            self.selected.pos.y = new_y
            self.on_redraw()
        else:
            super().on_mouse_drag(x, y, key)