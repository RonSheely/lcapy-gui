from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from lcapygui.ui.uimodelbase import Thing
from lcapygui.ui.tk.menu_popup import make_popup, unmake_popup
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
        self.crosshair.thing = thing
        if self.ui.debug:
            print(f"Crosshair mode: {self.crosshair.thing}")
        # redraw crosshair
        self.crosshair.undraw()
        self.crosshair.draw()
        self.ui.refresh()

    def on_add_con(self, thing):
        # Set crosshair mode to the component type
        self.on_add_cpt(thing)

    def on_mouse_release(self):
        """
        Performs operations on mouse release
        """
        if self.ui.debug:
            print("mouse release")

        # If finished placing a component, stop placing
        if self.new_component is not None:
            # If the crosshair has not moved, then instantly place the component at the current position
            if self.crosshair.x == self.new_component.gcpt.node1.pos.x and self.crosshair.y == self.new_component.gcpt.node1.pos.y:
                self.node_move(self.new_component.gcpt.node1, self.crosshair.x - 1, self.crosshair.y)
                self.node_move(self.new_component.gcpt.node2, self.crosshair.x + 1, self.crosshair.y)
                self.history.append(HistoryEvent("A", self.new_component))
            else:
                # Reset crosshair mode
                self.crosshair.thing = None

                self.merge_nodes(self.new_component)

                # If created component is a dynamic wire, split to component parts.
                if self.new_component.gcpt.type == "DW":
                    self.new_component.gcpt.convert_to_wires(self)
                else:
                    self.history.append(HistoryEvent("A", self.new_component))

        elif self.selected is not None:
            if self.cpt_selected:  # Moving a component
                # Merge component with existing nodes if present
                self.merge_nodes(self.selected)

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
            else:
                for cpt in self.selected.connected:
                    self.merge_nodes(cpt, self.selected)

                node_position = [(self.selected.pos.x, self.selected.pos.y)]
                self.history.append(
                    HistoryEvent("M", self.selected, self.node_positions, node_position)
                )

        self.dragged = False
        self.new_component = None

        self.on_redraw()

    def merge_nodes(self, current_cpt, ignore_node=None):
        """
        Merges the current selected node with the nearest node of the current component
        Paramaters
        ==========
        current_cpt
            to merge node into
        ignore_node
            Node to ignore, if it is present in the current component.
        """
        cpt = current_cpt.gcpt

        for node_count, cpt_node in enumerate(cpt.nodes):
            # Use given node if present, otherwise loop through all nodes
            for node in  self.circuit.nodes.values():

                print(f"checking node {node.name} {node.pos.x, node.pos.y}") if self.ui.debug else None

                if cpt_node.name == node.name or node == ignore_node:
                    print(f" -> warning same node {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}, same node") if self.ui.debug else None
                elif abs(node.pos.x - cpt_node.pos.x) < 0.1 and abs(node.pos.y - cpt_node.pos.y) < 0.1:
                    print(f" -> overwriting {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}") if self.ui.debug else None
                    node.connected.extend(cpt_node.connected)
                    cpt.nodes[node_count] = node
                    break
                else:
                    print(f" -> cannot merge {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}, too far apart") if self.ui.debug else None

    def on_left_click(self, x, y):
        # Destroy popup menu
        unmake_popup(self.ui)
        # Select component under mouse if not placing a component
        if self.crosshair.thing == None:
            self.on_select(x, y)

            if self.cpt_selected:
                cpt = self.selected
                if self.ui.debug:
                    print("Selected " + cpt.name)

        mouse_x, mouse_y = self.snap(x, y)

        if self.crosshair.thing != None and self.new_component is None: # If the component has not been created, create it at the current position
            print(self.crosshair.thing.kind)
            kind = (
                "-" + self.crosshair.thing.kind
                if self.crosshair.thing.kind != ""
                else ""
            )
            self.new_component = self.thing_create(
                self.crosshair.thing.cpt_type,
                mouse_x,
                mouse_y,
                mouse_x + self.preferences.scale,       # Have to be set to something larger because components now
                mouse_y,                                #   scale to the initial size of the component.
                kind=kind,
            )


    def on_left_double_click(self, x, y):
        self.on_select(x, y)
        if self.cpt_selected and self.selected.gcpt.type == "DW":
            self.history.append(HistoryEvent("D", self.selected))
            self.selected.gcpt.convert_to_wires(self)
        else:
            super().on_left_double_click(x, y)

    def on_right_click(self, x, y):
        self.on_select(x, y)

        if self.new_component is not None:
            self.cpt_delete(self.new_component)
            self.new_component = None
        # Show right click menu if not placing a component
        if self.crosshair.thing is None:
            # If a component is selected
            if self.selected and self.cpt_selected:
                # show the conponent popup
                make_popup(self.ui, self.selected.gcpt.menu_items)
            else: # if all else fails, show the paste popup
                if self.clipboard is None:
                    make_popup(self.ui, ["!edit_paste"])
                else:
                    make_popup(self.ui, ["edit_paste"])

        # clear current placed component on right click
        self.crosshair.thing = None


    def on_mouse_move(self, mouse_x, mouse_y):
        # Snap mouse to grid
        mouse_x, mouse_y = self.snap(mouse_x, mouse_y, True if self.new_component is None else False)

        self.crosshair.update((mouse_x, mouse_y))

    def snap(self, mouse_x, mouse_y, snap_to_component = False):
        """
        Snaps the x and y positions to the grid or to a component
        Parameters
        ==========
        mouse_x : float
        mouse_y : float
        snap_to_component : bool
            Determines if coords will snap to the selected component

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
            if (abs(mouse_x - snap_x) < 0.2 * self.preferences.grid_spacing and abs(mouse_y - snap_y) < 0.2 * self.preferences.grid_spacing) or not self.selected or not snap_to_component:
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
        for node in self.circuit.nodes.values(): # TODO: Fix snapping to components with more than 2 nodes.
            if abs(mouse_x - node.x) < 0.2 * self.preferences.grid_spacing and abs(mouse_y - node.y) < 0.2 * self.preferences.grid_spacing:
                return node.x, node.y
        return mouse_x, mouse_y

    def on_mouse_drag(self, mouse_x, mouse_y, key):
        """
        Performs operations when the user drags the mouse on the canvas.

        Explanation
        ===========
        If a chosen component is not created, it will create a new one at the current position
        If that component already exists, it will move the second node to the mouse position.

        It the chosen thing is a node, it will move that node to the current mouse position
        otherwise, it will attempt to drag a chosen component

        Parameters
        ==========
        mouse_x: float
            x position of the mouse
        mouse_y : float
            y position of the mouse
        key : str
            String representation of the pressed key.


        """

        mouse_x, mouse_y = self.snap(mouse_x, mouse_y)

        # Check if we are currently placing a component
        if self.crosshair.thing != None:
            # If the component has not been created, create it at the current position
            if self.new_component is not None:
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
                    self.node_positions = [(self.selected.pos.x, self.selected.pos.y)]
                self.node_move(self.selected, mouse_x, mouse_y)

    def on_mouse_scroll(self, scroll_direction, mouse_x, mouse_y):
        """
        Performs operations on mouse scroll
        Parameters
        ==========
        scroll_direction : str
        mouse_x : float
        mouse_y : float
        """
        if self.selected and self.cpt_selected:
            # rotate the component
            angle = 90 if scroll_direction == "up" else -90
            self.rotate(self.selected, angle)
            self.on_redraw()

    def on_cut(self):
        if self.selected is None:
            return
        if not self.cpt_selected:
            return
        self.cut(self.selected)
        self.ui.refresh()

    def on_delete(self):
        """
        If a component is selected, delete it, then redraw and refresh the UI
        """
        if self.selected is None:
            return
        if not self.cpt_selected:
            # Handle node deletion later
            return

        self.delete(self.selected)
        self.ui.refresh()

    def on_paste(self):
        if self.clipboard is None:
            if self.ui.debug:
                print("Nothing to paste")
            return

        if self.ui.debug:
            print("Pasting " + self.clipboard.name)
        # Generate new thing from clipboard
        paste_thing = Thing(None, None, self.clipboard.type, "")
        self.on_add_cpt(paste_thing)

        self.ui.refresh()
