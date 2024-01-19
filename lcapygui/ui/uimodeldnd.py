from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from lcapygui.ui.uimodelbase import Thing
from lcapygui.ui.tk.menu_popup import make_popup, unmake_popup
from lcapygui.components.picture import Picture
from .cross_hair import CrossHair


class UIModelDnD(UIModelMPH):
    """
    UIModelDnD

    Attributes
    ==========
    crosshair : CrossHair
        A crosshair for placing and moving components
    new_component : lcapygui.mnacpts.cpt or None
        The component currently being placed by the CrossHair
    node_positions : list of tuples or None
        Used for history, stores the node positions of the component or node before being moved

    """

    def __init__(self, ui):
        super(UIModelDnD, self).__init__(ui)
        self.crosshair = CrossHair(self)
        self.new_component = None
        self.node_positions = None

    def on_add_cpt(self, thing):
        """
        Configures crosshair for component creation.

        Parameters
        ----------
        thing
            The component to create

        Notes
        -----
        Saves the 'thing' (essentially a component type) to the crosshair, which dictates its appearance, and
        is referenced later in :func:`on_left_click` to determine if the component should be placed.

        The crosshair is then redrawn to reflect the new component type.

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
        """
        Configures crosshair for component creation.

        Parameters
        ----------
        thing
            The component to create

        Notes
        -----
        This method calls :func:`on_add_cpt` to configure the crosshair for component creation. Added for backwards
        compatibility with :mod:`lcapygui.ui.uimodelmph`.

        """
        # Set crosshair mode to the component type
        self.on_add_cpt(thing)

    def on_mouse_release(self, key=None):
        """
        Performs operations on mouse release

        Parameters
        ----------
        key : str or None
            String representation of the pressed key.

        Notes
        -----
        If a component is being placed, it will be placed at the current position.

        - If the crosshair has not moved since the component was created, a fixed size component will be placed.
        - Otherwise, we can assume the component has moved to its preferred position.

        Both cases will save to history.

        Pressing the 'shift' key will allow continual placing of components, otherwise the crosshair is reset to default

        If no component is being created, a component or node may have been moved. In this case, the component will be
        merged with any nearby nodes, and the new position will be saved to history.

        """
        if self.ui.debug:
            print(f"left mouse release. key: {key}")

        # If finished placing a component, stop placing
        if self.new_component is not None:
            # If the crosshair has not moved, then instantly place the component at the current position
            if self.crosshair.x == self.new_component.gcpt.node1.pos.x and self.crosshair.y == self.new_component.gcpt.node1.pos.y:
                self.node_move(self.new_component.gcpt.node1, self.crosshair.x - 1, self.crosshair.y)
                self.node_move(self.new_component.gcpt.node2, self.crosshair.x + 1, self.crosshair.y)
                self.history.append(HistoryEvent("A", self.new_component))
            else:  # Otherwise, confirm the component placement in its current position, and save to history
                self.merge_nodes(self.new_component)

                # If created component is a dynamic wire, split to component parts.
                if self.new_component.gcpt.type == "DW":
                    self.new_component.gcpt.convert_to_wires(self)
                else:
                    self.history.append(HistoryEvent("A", self.new_component))

            # Allow continual placing of components if the shift key is pressed
            if key != 'shift':
                # Reset crosshair mode
                self.crosshair.thing = None
            # Clear up new_component to avoid confusion
            self.new_component = None

        elif self.selected is not None:
            if self.cpt_selected and self.node_positions is not None:  # Moving a component
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


        # Redraw screen for accurate display of labels
        self.on_redraw()
        # Used to determine if a component or node is being moved in the on_mouse_drag method
        self.dragged = False

    def merge_nodes(self, current_cpt, ignore_node=None):
        """
        Merges the current selected component with any existing nearby nodes

        Paramaters
        ----------
        current_cpt
            to merge node into
        ignore_node
            Node to ignore, if it is present in the current component.

        Notes
        -----
        For each node the current component is attached to, search for a nearby node.
            If such a node exists, and it is not the same node, delete the existing node from the component and add the
            new-found node. Then, ensure the node is aware of the new component is connected to.

        """
        cpt = current_cpt.gcpt

        for node_count, cpt_node in enumerate(cpt.nodes):
            # Use given node if present, otherwise loop through all nodes
            for node in self.circuit.nodes.values():

                print(f"checking node {node.name} {node.pos.x, node.pos.y}") if self.ui.debug else None

                if cpt_node.name == node.name or node == ignore_node:
                    print(
                        f" -> warning same node {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}, same node") if self.ui.debug else None
                elif abs(node.pos.x - cpt_node.pos.x) < 0.1 and abs(node.pos.y - cpt_node.pos.y) < 0.1:
                    print(
                        f" -> overwriting {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}") if self.ui.debug else None
                    node.connected.extend(cpt_node.connected)
                    cpt.nodes[node_count] = node
                    break
                else:
                    print(
                        f" -> cannot merge {cpt_node.name} {cpt_node.pos.x, cpt_node.pos.y}, too far apart") if self.ui.debug else None

    def split_nodes(self, current_cpt, current_node):
        """
        Removes the given node from the component, and removes the component from the node
        Then creates a new node at the position and assigns that node to the component

        Parameters
        ----------
        current_cpt
        node

        """
        new_cpt = self.thing_create(
            current_cpt.gcpt.type,
            current_cpt.gcpt.node1.x,
            current_cpt.gcpt.node1.y,
            current_cpt.gcpt.node2.x,
            current_cpt.gcpt.node2.y

        )
        self.delete(current_cpt)

        for node in new_cpt.nodes:
            if node.pos.x == current_node.pos.x and node.pos.y == current_node.pos.y:
                return node

    def on_left_click(self, mouse_x, mouse_y):
        """
        Performs operations on left click

        Parameters
        ----------
        mouse_x : float
            x position of the mouse on screen
        mouse_y : float
            y position of the mouse on screen

        Notes
        -----
        If not placing a component, it will attempt to select a component or node under the mouse.
        otherwise, if a component is being placed, the first node will be placed at the current position.


        """
        # Destroy popup menu
        unmake_popup(self.ui)

        mouse_x, mouse_y = self.snap(mouse_x, mouse_y, True)

        # Select component under mouse if not placing a component
        if self.crosshair.thing == None:
            self.on_select(mouse_x, mouse_y)
            if self.selected is not None:
                if self.cpt_selected:
                    cpt = self.selected.gcpt
                    if self.ui.debug:
                        print("Selected component " + cpt.name)
                else:
                    if self.ui.debug:
                        print("Selected node " + self.selected.name)


        elif self.new_component is None:  # If the component has not been created, create it at the current position
            if self.ui.debug:
                print("creating new: " + self.crosshair.thing.kind)
            kind = (
                "-" + self.crosshair.thing.kind
                if self.crosshair.thing.kind != ""
                else ""
            )
            self.new_component = self.thing_create(
                self.crosshair.thing.cpt_type,
                mouse_x,
                mouse_y,
                mouse_x + self.preferences.scale,
                # Have to be set to something larger because components now scale
                # to the initial size of the component.
                mouse_y,
                kind=kind,
            )

    def on_left_double_click(self, mouse_x, mouse_y):
        """
        Performs operations on left double click

        Parameters
        ----------
        mouse_x : float
            x position of the mouse on screen
        mouse_y : float
            y position of the mouse on screen

        Notes
        -----
        Attempts to select a component under the mouse.
        If the component is a dynamic wire, it will be converted to a regular wire
        Otherwise, it will default to UIModelMPH on_left_double_click behaviour.

        """
        self.on_select(mouse_x, mouse_y)
        if self.cpt_selected and self.selected.gcpt.type == "DW":
            self.history.append(HistoryEvent("D", self.selected))
            self.selected.gcpt.convert_to_wires(self)
        else:
            super().on_left_double_click(mouse_x, mouse_y)

    def on_right_click(self, mouse_x, mouse_y):
        """
        Performs operations on right click

        Parameters
        ----------
        mouse_x : float
            x position of the mouse on screen
        mouse_y : float
            y position of the mouse on screen

        Notes
        -----
        If placing a component, it cancels the place operation and deletes the component if it exists.
        otherwise, it will attempt to show a popup-menu
        - Component popup menu if a component is selected
        - Paste popup menu if no component is selected

        """
        self.on_select(mouse_x, mouse_y)

        if self.new_component is not None:
            self.cpt_delete(self.new_component)
            self.new_component = None
        # Show right click menu if not placing a component
        if self.crosshair.thing is None:
            # If a component is selected
            if self.selected and self.cpt_selected:
                # show the comonent popup
                make_popup(self.ui, self.selected.gcpt.menu_items)
            else:  # if all else fails, show the paste popup
                if self.clipboard is None:
                    make_popup(self.ui, ["!edit_paste"])
                else:
                    make_popup(self.ui, ["edit_paste"])

        # clear current placed component on right click
        self.crosshair.thing = None

    def on_mouse_move(self, mouse_x, mouse_y):
        """
        Performs operations on mouse move

        Parameters
        ----------
        mouse_x : float
            x position of the mouse on screen
        mouse_y : float
            y position of the mouse on screen

        Notes
        -----
        Updates the crosshair position based on the mouse position.
        Will attempt to snap to the grid or to a component if the snap grid is enabled.

        """
        # Snap mouse to grid if enabled
        if self.preferences.snap_grid:
            mouse_x, mouse_y = self.snap(mouse_x, mouse_y, True if self.new_component is None else False)

        self.crosshair.update((mouse_x, mouse_y))

    def snap(self, mouse_x, mouse_y, snap_to_component=False):
        """
        Snaps the x and y positions to the grid or to a component

        Parameters
        ----------
        mouse_x : float
            x position of the mouse on screen
        mouse_y : float
            y position of the mouse on screen
        snap_to_component : bool
            Determines if coords will snap to a selected component

        Returns
        -------
        tuple[float, float]
            The snapped x, y position

        Notes
        -----
        Will only attempt to snap if allowed in settings

        Will snap to the grid if the mouse is close to the grid position
        Otherwise, it will attempt to snap to the component itself to allow component selection.
        If no component is close enough, it will simply revert to snapping to the grid.

        """
        # Only snap if the snap grid is enabled
        if self.preferences.snap_grid:

            snap_x, snap_y = self.snap_to_grid(mouse_x, mouse_y)
            # Prioritise snapping to the grid if close, or if placing a component
            if (abs(mouse_x - snap_x) < 0.2 * self.preferences.grid_spacing and abs(
                    mouse_y - snap_y) < 0.2 * self.preferences.grid_spacing) or not self.selected or not snap_to_component:
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
            for node in self.circuit.nodes.values():
                if abs(mouse_x - node.x) < 0.2 * self.preferences.grid_spacing and abs(
                        mouse_y - node.y) < 0.2 * self.preferences.grid_spacing:
                    return node.x, node.y
        return mouse_x, mouse_y

    def on_mouse_drag(self, mouse_x, mouse_y, key=None):
        """
        Performs operations when the user drags the mouse on the canvas.

        Explanation
        ------------
        If a chosen component is not created, it will create a new one at the current position
        If that component already exists, it will move the second node to the mouse position.

        It the chosen thing is a node, it will move that node to the current mouse position
        otherwise, it will attempt to drag a chosen component

        Parameters
        ----------
        mouse_x: float
            x position of the mouse
        mouse_y : float
            y position of the mouse
        key : str
            String representation of the pressed key.

        Notes
        -----
        If placing a component, and have placed the first node already, the second node will be moved to the current snap position
        If a preexisting component is selected, it will be moved with the mouse.
        Otherwise, if a node is selected, the node will be moved to the new position instead.

        """
        mouse_x, mouse_y = self.snap(mouse_x, mouse_y)

        # Check if we are currently placing a component, and have already placed the first node
        if self.crosshair.thing != None and self.new_component is not None:
                self.node_positions = [
                    (node.pos.x, node.pos.y) for node in self.new_component.nodes
                ]
                self.node_move(self.new_component.gcpt.node2, mouse_x, mouse_y)

        elif self.selected:
            # If a component is selected, move it with the mouse
            if self.cpt_selected:
                super().on_mouse_drag(mouse_x, mouse_y, key)

            else:

                # move selected node
                if not self.dragged:
                    self.dragged = True
                    # To save history, save first component position
                    self.node_positions = [(self.selected.pos.x, self.selected.pos.y)]
                if key == "shift":
                    self.split_nodes()
                self.node_move(self.selected, mouse_x, mouse_y)

    def on_mouse_scroll(self, scroll_direction, mouse_x, mouse_y):
        """
        Performs operations on mouse scroll

        Parameters
        ----------
        scroll_direction : str
            String representation of the scroll direction
        mouse_x: float
            x position of the mouse
        mouse_y : float
            y position of the mouse

        Notes
        -----
        Rotates the selected component based on scroll direction. Currently only supports on 90 degree increments.
        """
        if self.selected and self.cpt_selected:
            # rotate the component
            angle = 90 if scroll_direction == "up" else -10
            self.rotate(self.selected, angle)
            self.selected.gcpt.undraw()
            self.selected.gcpt.draw(self)

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
