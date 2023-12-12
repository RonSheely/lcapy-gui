from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from .cross_hair import CrossHair


class UIModelDnD(UIModelMPH):

    """
    UIModelDnD

    Attributes
    ==========
    crosshair : CrossHair
        A crosshair for placing and moving components
    new_component : lcapygui.mnacpts.cpt or None

    """

    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)
        self.crosshair = CrossHair(self)
        self.new_component = None

    def on_add_cpt(self, thing):
        """
        Configures crosshair for component creation
        Parameters
        ==========
        thing
            The component to create
        """
        # Set crosshair mode to the component type
        self.crosshair.mode = thing.cpt_type
        if self.ui.debug:
            print(f"Crosshair mode: {self.crosshair.mode}")
        # redraw crosshair
        self.crosshair.undraw()
        self.crosshair.draw()
        self.ui.refresh()

    def on_mouse_release(self):
        """
        Performs operations on mouse release
        """
        if self.ui.debug:
            print("mouse release")

        # If finished placing a component, stop placing
        if self.new_component is not None:
            # If the component is too small, delete it
            if self.new_component.gcpt.length < 0.2:
                self.cpt_delete(
                    self.new_component
                )  # uses cpt_delete to avoid being added to history
            else:
                # Reset crosshair mode
                self.crosshair.mode = "default"

                # If created component is a dynamic wire, split to component parts.
                if self.new_component.gcpt.type == "DW":
                    self.new_component.gcpt.convert_to_wires(self)
                else:
                    self.history.append(HistoryEvent("A", self.new_component))

        elif self.selected is not None:
            if self.cpt_selected:   # Moving a component
                # Update move history
                node_positions = [
                    (node.pos.x, node.pos.y) for node in self.selected.nodes
                ]
                self.history.append(
                    HistoryEvent(
                        "M", self.selected, self.node_positions, node_positions
                    )
                )
            # Moving a node
            elif self.selected.connected is not None:
                # Treat as moving a single attached component
                node_positions = [
                    (node.pos.x, node.pos.y) for node in self.selected.connected[0].nodes
                ]

                self.history.append(
                    HistoryEvent("M", self.selected.connected[0], self.node_positions, node_positions)
                )

        self.dragged = False
        self.new_component = None

        self.on_redraw()

    def on_left_click(self, x, y):
        if self.crosshair.mode == "default":
            super().on_left_click(x, y)

    def on_left_double_click(self, x, y):
        self.on_select(x, y)
        if self.cpt_selected and self.selected.gcpt.type == "DW":
            self.history.append(HistoryEvent("D", self.selected))
            self.selected.gcpt.convert_to_wires(self)
        else:
            super().on_left_double_click(x, y)

    def on_right_click(self, x, y):
        self.crosshair.mode = "default"
        if self.new_component is not None:
            self.cpt_delete(self.new_component)
            self.new_component = None

    def on_mouse_move(self, mouse_x, mouse_y):
        # Snap mouse to grid
        mouse_x, mouse_y = self.snap(mouse_x, mouse_y)

        self.crosshair.update((mouse_x, mouse_y))

    def snap(self, mouse_x, mouse_y):
        """
        Snaps the x and y positions to the grid or to a component
        Parameters
        ==========
        mouse_x : float
        mouse_y : float

        Returns
        =======
        float
            The snapped x, y position

        """
        # Only snap if the snap grid is enabled
        if self.preferences.snap_grid:
            snapped = False
            snap_x, snap_y = self.snap_to_grid(mouse_x, mouse_y)
            # Prioritise snapping to the grid if close, or if placing a component
            if (
                abs(mouse_x - snap_x) < 0.2 and abs(mouse_y - snap_y) < 0.2
            ) or self.selected:
                return snap_x, snap_y
            else:
                # if not close grid position, attempt to snap to component
                snapped = False
                for cpt in self.circuit.elements.values():
                    if (
                        cpt.gcpt is not self
                        and cpt.gcpt.distance_from_cpt(mouse_x, mouse_y) < 0.2
                    ):
                        mouse_x, mouse_y = self.snap_to_cpt(mouse_x, mouse_y, cpt)
                        snapped = True
                # If no near components, snap to grid
                if not snapped:
                    return snap_x, snap_y
        return mouse_x, mouse_y

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

        mouse_x, mouse_y = self.snap(mouse_x, mouse_y)

        if self.crosshair.mode != "default":
            if self.new_component is None:
                self.new_component = self.thing_create(
                    self.crosshair.mode, mouse_x, mouse_y, mouse_x + 0.1, mouse_y
                )
            else:
                self.node_positions = [
                    (node.pos.x, node.pos.y) for node in self.new_component.nodes
                ]
                self.node_move(self.new_component.gcpt.node2, mouse_x, mouse_y)

        elif self.selected:
            if self.cpt_selected:
                super().on_mouse_drag(mouse_x, mouse_y, key)

            else:
                # move selected node
                if not self.dragged:
                    self.dragged = True
                    # To save history, save first component position
                    self.node_positions = [(node.pos.x, node.pos.y)
                                   for node in self.selected.connected[0].nodes]
                self.node_move(self.selected, mouse_x, mouse_y)
