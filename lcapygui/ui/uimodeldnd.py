from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH


class Crosshair:
    """
    A crosshair object for moving components on the canvas
    """

    def __init__(self, ui, mouse_x, mouse_y):
        """
        Initialise the crosshair class
        :param ui: The UI element
        :param mouse_x: mouse x position
        :param mouse_y: mouse y position

        """
        self.sketcher = ui.sketcher
        self.patch = None
        self.x = mouse_x
        self.y = mouse_y

    def position(self):
        """
        Gets the position of the crosshair
        :return: x, y position of the crosshair
        :rtype: tuple[float, float]
        """
        return self.x, self.y

    def set_position(self, mouse_x, mouse_y):
        """
        Sets the position of the crosshair
        :param float mouse_x: mouse x position
        :param float mouse_y: mouse y position
        """
        self.x = mouse_x
        self.y = mouse_y

    def draw(self, size=0.2):
        """
        Draws the crosshair on the canvas
        :param float size: the total height of the crosshair
        """
        self.patch = self.sketcher.draw_line(
            self.x,
            self.y - size / 2,
            self.x,
            self.y + size / 2,
            color="black",
            alpha=0.5,
        )

    def remove(self):
        """
        Removes the crosshair from the canvas
        """
        self.patch.remove(self.patch)


class UIModelDnD(UIModelMPH):
    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)

    def on_add_cpt(self, cpt_key):
        """
        Adds a component to the circuit after a key is pressed

        Explanation
        ===========
        If there are cursors present, it will place a component between them
        otherwise, the component will follow the cursor until the user left clicks

        :param str cpt_key: key pressed
        """
        if self.ui.debug:
            print(f"adding component at mouse position: {self.mouse_position}")
        # Get mouse positions
        mouse_x = self.mouse_position[0]
        mouse_y = self.mouse_position[1]
        if len(self.cursors) == 0:
            # create a new component at the mouse position
            self.cpt_create(cpt_key, mouse_x - 2, mouse_y, mouse_x + 2, mouse_y)
            self.ui.refresh()

            # Select the newly created component
            self.follow_mouse = True

        else:
            # add a new cursor at the grid position closest to the mouse
            self.add_cursor(round(mouse_x), round(mouse_y))

            # add the component like normal
            super().on_add_cpt(cpt_key)

    def on_left_click(self, x, y):
        """
        Performs operations on left-click

        Explanation
        ===========
        This function is called when the user left-clicks on the canvas.
        If a component is currently being dragged, it will drop the component
        Otherwise, it selects the component at the mouse position

        Parameters
        ==========
        :param float x: x position of the mouse
        :param float y: y position of the mouse
        """

        self.on_select(x, y)

        # TODO: instead of appearing at the cursor, the user should be able to drag it from a sidebar
        # drop the component if being dragged
        if self.follow_mouse:
            if self.ui.debug:
                print("dropped component (%s, %s)" % (x, y))
            self.follow_mouse = False
            self.cursors.remove()
            self.unselect()

        # draw cursors if selecting a component
        elif self.cpt_selected:
            cpt = self.selected
            if self.ui.debug:
                print("Selected " + cpt.name)
            self.cursors.remove()
            self.add_cursor(cpt.gcpt.node1.pos.x, cpt.gcpt.node1.pos.y)
            node2 = cpt.gcpt.node2
            if node2 is not None:
                self.add_cursor(node2.pos.x, node2.pos.y)
        # if not selecting anything, add a new node
        else:
            if self.ui.debug:
                print("Add node at (%s, %s)" % (x, y))
            self.cursors.remove()  # TODO: stop clearing nodes on click when node-dragging is implemented
            self.on_add_node(x, y)

    def on_right_click(self, x, y):
        """
        performs operations on right-click

        Explanation
        ===========
        This function is called when the user right-clicks on the canvas.
        If no component is selected, it will clear the cursors from the screen.
        Otherwise, it will show the selected components properties dialogue
        :param float x: x position of the mouse
        :param float y: y position of the mouse
        """
        super().on_right_click(x, y)
        self.unselect()

    def on_mouse_drag(self, mouse_x, mouse_y):
        """
        Allows for dragging of components

        Explanation
        ===========
        When an object is selected, it will follow the cursor.
        :param mouse_x:
        :param mouse_y:
        :return:
        """

        if not self.selected or not self.cpt_selected:
            return
        cpt = self.selected

        if not self.dragged:
            self.dragged = True
            self.last_pos = self.snap_to_grid(mouse_x + 1, mouse_y + 1)
            node_positions = [(node.pos.x, node.pos.y) for node in cpt.nodes]
            self.history.append(HistoryEvent("M", cpt, node_positions))

        # Calculate the difference of the points from the mouse location
        x0, y0 = self.last_pos
        self.last_pos = self.snap_to_grid(mouse_x + 1, mouse_y + 1)

        x1, y1 = mouse_x - x0 + 1, mouse_y - y0 + 1

        update = False
        # Move nodes, and snap them to the grid
        for node in cpt.nodes:
            new_x, new_y = self.snap_to_grid(node.pos.x + x1, node.pos.y + y1)
            if new_x != node.pos.x or new_y != node.pos.y:
                update = True  # only update if the component actually moved
            node.pos.x = new_x
            node.pos.y = new_y

        # update screen when component moved.
        if update:
            self.on_redraw()

            if self.ui.debug:
                print("redrawing screen")
