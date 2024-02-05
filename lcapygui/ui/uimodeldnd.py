from lcapygui.ui.cursor import Cursor
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
    ----------
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
        if len(self.cursors) >= 2:
            self.create_component_between_cursors(thing)
            self.cursors.remove()
        else:
            if self.ui.debug:
                print(f"Crosshair mode: {self.crosshair.thing}")
            self.crosshair.update(thing=thing)

        # # Set crosshair mode to the component type
        # self.crosshair.thing = thing
        # if self.ui.debug:
        #     print(f"Crosshair mode: {self.crosshair.thing}")
        # # redraw crosshair
        # self.crosshair.undraw()
        # self.crosshair.draw()
        #
        # self.ui.refresh()

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
            self.node_positions = [
                (node.pos.x, node.pos.y) for node in self.new_component.nodes
            ]
            # If the crosshair has not moved, then instantly place the component at the current position
            if self.crosshair.x == self.new_component.gcpt.node1.pos.x and self.crosshair.y == self.new_component.gcpt.node1.pos.y:
                self.node_move(self.new_component.gcpt.node1, self.crosshair.x - 1, self.crosshair.y)
                self.node_move(self.new_component.gcpt.node2, self.crosshair.x + 1, self.crosshair.y)
                self.history.append(HistoryEvent("A", self.new_component))
            else:  # Otherwise, confirm the component placement in its current position, and save to history
                # If created component is a dynamic wire, split to component parts.
                if self.new_component.gcpt.type == "DW":
                    self.new_component.gcpt.convert_to_wires(self)
                else:
                    self.history.append(HistoryEvent("A", self.new_component))

                join_args = self.node_join(self.new_component.gcpt.node2)
                if join_args is not None:
                    # Add the join event to history
                    self.history.append(HistoryEvent('J', from_nodes=join_args[0], to_nodes=join_args[1], cpt=join_args[2]))

            # Allow continual placing of components if the shift key is pressed
            if key != 'shift':
                # Reset crosshair mode
                self.crosshair.thing = None
            # Clear up new_component to avoid confusion
            self.new_component = None

        elif self.selected is not None:
            if self.cpt_selected and self.node_positions is not None:  # Moving a component
                # Merge component with existing nodes if present
                #self.node_merge(self.selected)

                # Update move history
                node_positions = [
                    (node.pos.x, node.pos.y) for node in self.selected.nodes
                ]
                self.history.append(
                    HistoryEvent(
                        "M", self.selected, self.node_positions, node_positions
                    )
                )
                self.node_positions = None
            # Moving a node
            elif self.node_positions is not None:
                self.crosshair.thing = None
                node_position = [(self.selected.pos.x, self.selected.pos.y)]
                self.history.append(
                    HistoryEvent("M", self.selected, self.node_positions, node_position)
                )
                self.node_positions = None
                # Join selected node if close
                join_args = self.node_join(self.selected)
                if join_args is not None:
                    # Add the join event to history
                    self.history.append(
                        HistoryEvent('J', from_nodes=join_args[0], to_nodes=join_args[1], cpt=join_args[2]))


        # Redraw screen for accurate display of labels
        #self.on_redraw()
        # Used to determine if a component or node is being moved in the on_mouse_drag method
        self.dragged = False


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

        # Destroy all Popups
        unmake_popup(self.ui)


        # Select component/node under mouse
        self.on_select(mouse_x, mouse_y)

        # If a component is selected, do nothing
        if self.cpt_selected:
            if self.ui.debug:
                print("Selected component " + self.selected.gcpt.name)
            return

        # If a node is selected, update mouse_x, mouse_y to that nodes position
        if self.selected:
            if self.ui.debug:
                print("Selected node " + self.selected.name)
            mouse_x, mouse_y = self.selected.pos.x, self.selected.pos.y
        else: # Otherwise default to the crosshair position
            mouse_x, mouse_y = self.crosshair.position

        # Attempt to add a new cursor


        # Just placed a cursor, add a new component if we want
        if self.on_add_cursor(mouse_x, mouse_y) and len(self.cursors) == 2 and self.crosshair.thing is not None:
            self.create_component_between_cursors()

    def create_component_between_cursors(self, thing=None):
        """
        Creates a component between the two cursors, if present

        Parameters
        ----------
        thing : Thing, optional
            Used to decide an arbitrary component type if provided,
                otherwise will default to the self.crosshair.thing if available

        Returns
        -------
        bool
            Returns True if a component could have been created
            - There are 2 cursors to create a component between
            - A thing was provided, or available from self.crosshair.thing

        Notes
        -----
        This method will still return True, even if the component creation was unsuccessful. It only checks if it is
            provided enough information to create a component to pass into the :func:`self.create` method.

        """
        if len(self.cursors) < 2:
            if self.ui.debug:
                print("Not enough cursors to create component")
            return False

        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        if thing is None and self.crosshair.thing is not None:
            thing = self.crosshair.thing
        else:
            if self.ui.debug:
                print("No-thing provided to decide component type")
            return False


        self.create(thing.cpt_type, x1, y1, x2, y2)

        self.ui.refresh()
        return True

    def on_add_cursor(self, mouse_x, mouse_y):

        # Create a new temporary cursor
        cursor = Cursor(self.ui, mouse_x, mouse_y)

        if len(self.cursors) == 0: # If no cursors, add positive one
            cursor.draw('red')
            self.cursors.append(cursor)
            if self.ui.debug:
                print("Adding positive cursor")
        elif len(self.cursors) == 1: # if one cursor, add negative one
            cursor.draw('blue')
            self.cursors.append(cursor)
            if self.ui.debug:
                print("Adding negative cursor")
        elif len(self.cursors) >= 2:  # if too many cursors, clear all
            self.cursors.remove()
            if self.ui.debug:
                print("Too many cursors, clearing all")
            self.ui.refresh()
            return False

        # Refresh UI
        self.ui.refresh()
        return True











        # # Destroy popup menu
        # unmake_popup(self.ui)
        # print(self.crosshair.thing)
        # # Select component under mouse if not placing a component
        # if self.crosshair.thing == None:
        #     self.on_select(mouse_x, mouse_y)
        #     if self.cpt_selected:
        #         cpt = self.selected.gcpt
        #         if self.ui.debug:
        #             print("Selected component " + cpt.name)
        #     else:
        #         if self.ui.debug:
        #             print("Selected node " + self.selected.name)
        #         self.on_add_node(mouse_x, mouse_y)
        #
        # elif self.new_component is None:  # If the component has not been created, create it at the current position
        #     if self.ui.debug:
        #         print("creating new: " + self.crosshair.thing.kind)
        #     kind = (
        #         "-" + self.crosshair.thing.kind
        #         if self.crosshair.thing.kind != ""
        #         else ""
        #     )
        #
        #     mouse_x, mouse_y = self.crosshair.position
        #     self.new_component = self.thing_create(
        #         self.crosshair.thing.cpt_type,
        #         mouse_x,
        #         mouse_y,
        #         mouse_x + self.preferences.scale,
        #         # Have to be set to something larger because components now scale
        #         # to the initial size of the component.
        #         mouse_y,
        #         kind=kind,
        #     )

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
        self.cursors.remove()
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
        closest_node = self.closest_node(mouse_x, mouse_y)
        # If the crosshair is not over a node, snap to the grid (if enabled)
        if closest_node is None:
            if self.preferences.snap_grid:
                mouse_x, mouse_y = self.snap(mouse_x, mouse_y,
                                             snap_to_component=True if self.crosshair.thing is None else False)
            # Update position and reset style
            self.crosshair.update(position=(mouse_x, mouse_y), style=None)
            print(self.crosshair.style)
        else:
            self.crosshair.style = 'node'

            # Update the crosshair position and set style to show it is over a node
            self.crosshair.update(position=(closest_node.pos.x, closest_node.pos.y), style='node')




        #
        # if self.crosshair.thing is not None and self.new_component is None:
        #     if self.closest_node(self.crosshair.x, self.crosshair.y) is not None:
        #         self.crosshair.style = 'node'
        #     else:
        #         self.crosshair.style = None
        #
        # self.crosshair.update((mouse_x, mouse_y))

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

        mouse_x, mouse_y = self.crosshair.position

        # Check if we are currently placing a component, and have already placed the first node
        if self.new_component is not None:

                if self.closest_node(self.crosshair.x, self.crosshair.y, self.new_component.gcpt.node2) is not None:
                    self.crosshair.style = 'node'
                else:
                    self.crosshair.style = None
                self.node_move(self.new_component.gcpt.node2, mouse_x, mouse_y)

        elif self.selected:
            # If a component is selected, move it with the mouse
            if self.cpt_selected:
                #print(self.selected.nodes)
                super().on_mouse_drag(mouse_x, mouse_y, key)

            else:

                # move selected node
                if not self.dragged:
                    self.dragged = True
                    # To save history, save first component position
                    self.node_positions = [(self.selected.pos.x, self.selected.pos.y)]
                if key == "shift":
                    print("Splitting nodes with shift not implemented yet, please use undo")

                if self.crosshair.thing is None:
                    # Show crosshair as node if close to a node
                    if self.closest_node(self.crosshair.x, self.crosshair.y, ignore=self.selected) is not None:
                        self.crosshair.style = 'node'
                    else:
                        self.crosshair.style = None

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
            angle = 90 if scroll_direction == "up" else -90
            self.rotate(self.selected, angle)
            self.selected.gcpt.undraw()
            self.selected.gcpt.draw(self)

    def on_cut(self):
        """
        If a component is selected, add it to the clipboard and remove it from the circuit

        """
        if not self.cpt_selected:
            return
        self.cut(self.selected)
        self.ui.refresh()

    def on_delete(self):
        """
        If a component is selected, delete it, then redraw and refresh the UI

        """
        if not self.cpt_selected:
            # Handle node deletion later
            return

        self.delete(self.selected)
        self.on_redraw()
        self.ui.refresh()

    def on_paste(self):
        """
        If the clipboard is not empty, create a new component from the clipboard and add it to the circuit

        """
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

