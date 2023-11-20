from lcapygui.ui.uimodelmph import UIModelMPH


class UIModelDnD(UIModelMPH):

    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)

    def on_add_cpt(self, cpt_key):
        """
        Adds a component to the circuit after a key is pressed

        If there are cursors present, it will place a component between them
        otherwise, the component will follow the cursor until the user left clicks

        :param cpt_key: key pressed
        :return: None
        """
        if self.ui.debug:
            print(f"adding component at mouse position: {self.mouse_position}")
        # Get mouse positions
        mouse_x = self.mouse_position[0]
        mouse_y = self.mouse_position[1]
        if len(self.cursors) > 0:
            # add a new cursor at the grid position closest to the mouse
            self.add_cursor(round(mouse_x), round(mouse_y))

            # add the component like normal
            super().on_add_cpt(cpt_key)
        else:
            # create a new component at the mouse position
            cpt = self.cpt_create(cpt_key, mouse_x-2, mouse_y, mouse_x+2, mouse_y)
            self.ui.refresh()

            # Select the newly created component
            self.on_select(mouse_x, mouse_y)
            self.follow_mouse = True


    def on_left_click(self, x, y):

        # drop the component in place after clicking
        if self.follow_mouse:
            self.follow_mouse = False
            self.on_select(x, y)
            self.cursors.remove()
            # Add cursors to the component
            cpt = self.selected
            self.add_cursor(cpt.gcpt.node1.pos.x, cpt.gcpt.node1.pos.y)
            node2 = cpt.gcpt.node2
            if node2 is not None:
                self.add_cursor(node2.pos.x, node2.pos.y)
        else:
            super().on_left_click(x, y)

    def on_right_click(self, x, y):
        super().on_right_click(x, y)
        if not self.selected:
            self.unselect()



    def follow(self, x, y):
        """
        Follows the mouse with the selected component

        :param x: mouse x position
        :param y: mouse y position
        :return: None
        """
        if not self.selected or not self.cpt_selected or not self.follow_mouse:
            return
        cpt = self.selected
        self.last_pos = self.select_pos

        # Update position
        x0, y0 = self.last_pos
        self.last_pos = x, y

        # Update component
        for node in cpt.nodes:
            # TODO: handle snap
            node.pos.x += x - x0
            node.pos.y += y - y0

        self.on_redraw()
