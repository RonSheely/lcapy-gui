from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from .cross_hair import CrossHair


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
        self.crosshair = CrossHair(0, 0, self)
        self.new_component = None

    def on_add_cpt(self, thing):
        self.crosshair.mode = thing.cpt_type
        print(self.crosshair.mode)
        self.crosshair.undraw()
        self.crosshair.draw()
        self.ui.refresh()

    def on_mouse_release(self):
        super().on_mouse_release()

        # IF finished placing a component, stop placing
        if self.new_component is not None:
            # If the component is too small, delete it
            if self.new_component.gcpt.length < 0.2:
                self.cpt_delete(self.new_component)
            else:
                self.crosshair.mode = "default"
                if self.new_component.gcpt.type == "DW":
                    self.new_component.gcpt.convert_to_wires(self)

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
            if (abs(mouse_x - snap_x) < 0.2 and abs(mouse_y - snap_y) < 0.2) or self.selected:
                return snap_x, snap_y
            else:
                # if not close grid position, attempt to snap to component
                snapped = False
                for cpt in self.circuit.elements.values():
                    if cpt.gcpt is not self and cpt.gcpt.distance_from_cpt(mouse_x, mouse_y) < 0.2:
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
                self.node_move(self.new_component.gcpt.node2, mouse_x, mouse_y)

        elif self.selected and not self.cpt_selected:
            new_x, new_y = self.snap_to_grid(mouse_x, mouse_y)

            self.node_move(self.selected, new_x, new_y)
        else:
            super().on_mouse_drag(mouse_x, mouse_y, key)
