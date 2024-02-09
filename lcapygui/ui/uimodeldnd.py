from lcapygui.ui.cursor import Cursor
from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from lcapygui.ui.uimodelbase import Thing
from lcapygui.ui.tk.menu_popup import MenuPopup, MenuDropdown
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
        Configures crosshair and cursors for component creation.

        Parameters
        ----------
        thing
            The type of component to create

        Notes
        -----
        If there are two cursors, and there is no existing component, it will create a component between the cursors.

        Otherwise, it will initialise the crosshair to place a component of the given "thing" type.

        """
        # Only place a component between cursors if there are two cursors and no existing component between them
        if len(self.cursors) >= 2 and self.component_between_cursors() is None:
            self.create_component_between_cursors(thing)
        else:
            # Intialise crosshair to place a component of the given "thing" type
            self.cursors.remove()
            if self.ui.debug:
                print(f"Crosshair mode: {self.crosshair.thing}")
            self.crosshair.update(thing=thing)
        self.on_redraw()

    def on_add_con(self, thing):
        """
        Configures crosshair and cursors for component creation.

        Parameters
        ----------
        thing
            The component to create

        Notes
        -----
        This method calls :func:`on_add_cpt` to configure the crosshair and cursors for component creation.

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

        If placing a component with the mouse, we stop placing it, and add it to history.
            Will attempt to join the final point with any existing nodes if 'shift' is not pressed.

        Otherwise, if a move event has occurred
            It will stop the move event,


        """
        if self.ui.debug:
            print(f"left mouse release. key: {key}")

        # If finished placing a component, stop placing
        if self.new_component is not None:
            # Add the brand new component to history
            self.history.append(HistoryEvent("A", self.new_component))
            if key != "shift":
                join_args = self.node_join(self.new_component.gcpt.node2)
                if join_args is not None:
                    # Add the join event to history
                    self.history.append(
                        HistoryEvent('J', from_nodes=join_args[0], to_nodes=join_args[1], cpt=join_args[2]))

            # Reset crosshair mode
            self.crosshair.thing = None
            # Clear up new_component to avoid confusion
            self.new_component = None

        # If something is selected, and it has been moved
        elif self.selected is not None and self.node_positions is not None:
            if self.cpt_selected:  # Moving a component
                # Add moved component to history
                node_positions = [
                    (node.pos.x, node.pos.y) for node in self.selected.nodes
                ]
                self.history.append(
                    HistoryEvent(
                        "M", self.selected, self.node_positions, node_positions
                    )
                )
                self.node_positions = None

                if key == "shift":
                    for node in (self.selected.gcpt.node1, self.selected.gcpt.node2):
                        # Join selected node if close
                        join_args = self.node_join(node)
                        if join_args is not None:
                            # Add the join event to history
                            self.history.append(
                                HistoryEvent('J', from_nodes=join_args[0], to_nodes=join_args[1], cpt=join_args[2]))

            else:  # Moving a node
                # Add moved node to history
                node_position = [(self.selected.pos.x, self.selected.pos.y)]
                self.history.append(
                    HistoryEvent("M", self.selected, self.node_positions, node_position)
                )
                self.node_positions = None

                # If not denied, try to join
                if key == "shift":
                    # Join selected node if close
                    join_args = self.node_join(self.selected)
                    if join_args is not None:
                        # Add the join event to history
                        self.history.append(
                            HistoryEvent('J', from_nodes=join_args[0], to_nodes=join_args[1], cpt=join_args[2]))

        # Redraw screen for accurate display of labels
        self.on_redraw()
        # Used to determine if a component or node is being moved in the on_mouse_drag method
        self.dragged = False
        # Ensure node_positions is cleared to avoid duplicate history events
        self.node_positions = None

    def on_redraw(self):
        self.clear()
        self.redraw()
        self.cursors.draw()
        self.ui.refresh()

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
        self.unmake_popup()

        # Select component/node under mouse
        self.on_select(mouse_x, mouse_y)

        # If a component is selected, do nothing
        if self.cpt_selected:
            self.cursors.remove()
            self.add_cursor(self.selected.gcpt.node1.pos.x, self.selected.gcpt.node1.pos.y)
            node2 = self.selected.gcpt.node2
            if node2 is not None:
                self.add_cursor(node2.pos.x, node2.pos.y)
            if self.ui.debug:
                print("Selected component " + self.selected.gcpt.name)
            return

        # If a node is selected, update mouse_x, mouse_y to that nodes position
        if self.selected:
            if self.ui.debug:
                print("Selected node " + self.selected.name)
            mouse_x, mouse_y = self.selected.pos.x, self.selected.pos.y
        else:  # Otherwise default to the crosshair position
            mouse_x, mouse_y = self.crosshair.position


        # Attempt to add a new cursor
        if ((not self.is_popup()) and self.add_cursor(mouse_x, mouse_y) and
                (len(self.cursors) == 2) and (self.crosshair.thing is not None)):
            self.create_component_between_cursors()
            self.crosshair.thing = None
            self.cursors.remove()

        self.on_redraw()

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


        if thing is None:
            if self.crosshair.thing is None:
                if self.ui.debug:
                    print("No-thing provided to decide component type")
                return False
            thing = self.crosshair.thing

        self.cpt_create(thing.cpt_type, x1, y1, x2, y2)

        self.ui.refresh()
        return True

    def add_cursor(self, mouse_x, mouse_y):

        # Create a new temporary cursor
        cursor = Cursor(self.ui, mouse_x, mouse_y)

        if len(self.cursors) == 0:  # If no cursors, add positive one
            cursor.draw('red')
            self.cursors.append(cursor)
            if self.ui.debug:
                print("Adding positive cursor")
        elif len(self.cursors) == 1:  # if one cursor, add negative one
            cursor.draw('blue')
            self.cursors.append(cursor)
            if self.ui.debug:
                print("Adding negative cursor")
        elif len(self.cursors) >= 2:  # if too many cursors, clear all
            self.cursors.pop(0)
            self.cursors.append(cursor)
            if self.ui.debug:
                print("Too many cursors, clearing all")
            self.ui.refresh()
            return False

        # Refresh UI
        self.ui.refresh()
        return True

    def component_between_cursors(self):
        """
        Returns the component between the two cursors, if present

        Returns
        -------
        lcapygui.mnacpts.cpt or None
            The component between the two cursors, if present

        """
        if len(self.cursors) < 2:
            return None

        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        for cpt in self.circuit.elements.values():
            if (
                    cpt.gcpt is not self
                    and cpt.gcpt.distance_from_cpt(x1, y1) < 0.2
                    and cpt.gcpt.distance_from_cpt(x2, y2) < 0.2
            ):
                return cpt
        return None

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
        # Destroy any created component
        if self.new_component is not None:
            self.cpt_delete(self.new_component)
            self.new_component = None

        # Clear cursors
        self.cursors.remove()
        self.ui.refresh()

        # Show right a click menu if not placing a component and there are no cursors
        if self.crosshair.thing is None:
            self.on_select(mouse_x, mouse_y)
            # If a component is selected
            if self.selected and self.cpt_selected:
                # show the comonent popup
                self.make_popup(self.selected.gcpt.menu_items)
            elif self.selected:
                self.make_popup(["inspect_properties"])
            else:  # if all else fails, show the paste popup
                if self.clipboard is None:
                    self.make_popup(["!edit_paste"])
                else:
                    self.make_popup(["edit_paste"])

        # clear current placed component
        self.crosshair.thing = None

    def make_popup(self, menu_items):
        """
        Creates a popup menu

        Parameters
        ----------
        menu_items : list
            List of menu items to display in the popup

        """
        display_items = []
        for menu_item in menu_items:
            if menu_item[0] == '!':
                new_item = self.ui.menu_parts[menu_item[1:]]
                new_item.state = 'disabled'
            else:
                new_item = self.ui.menu_parts[menu_item]
                new_item.state = 'normal'
            display_items.append(new_item)

        self.ui.popup_menu = MenuPopup(
            MenuDropdown(
                "Right click",
                0,
                display_items,
            )
        )
        self.ui.popup_menu.make(self.ui, self.ui.level)
        self.ui.popup_menu.do_popup(self.ui.canvas.winfo_pointerx(), self.ui.canvas.winfo_pointery())

    def unmake_popup(self):
        """
        Destroys the popup menu
        """
        if self.ui.popup_menu is not None:
            self.ui.popup_menu.undo_popup()
            self.ui.popup_menu = None

    def is_popup(self):
        return self.ui.popup_menu is not None

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

        else:
            self.crosshair.style = 'node'

            # Update the crosshair position and set style to show it is over a node
            self.crosshair.update(position=(closest_node.pos.x, closest_node.pos.y), style='node')

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
            elif len(self.cursors) >= 1:
                xc = self.cursors[-1].x
                yc = self.cursors[-1].y
                if self.is_close_to(snap_x, xc):
                    return xc, snap_y
                if self.is_close_to(snap_y, yc):
                    return snap_x, yc
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
        # Get crosshair position
        mouse_x, mouse_y = self.crosshair.position

        # Check if we are currently placing a component, and have already placed the first node
        if self.new_component is not None:
            self.node_move(self.new_component.gcpt.node2, mouse_x, mouse_y)
            self.new_component.nodes[1].pos = self.new_component.gcpt.node2.pos
            return
        elif self.crosshair.thing is not None:  # Check if we need to place the first node
            if self.ui.debug:
                print("creating new: " + self.crosshair.thing.kind)

            kind = (
                "-" + self.crosshair.thing.kind
                if self.crosshair.thing.kind != ""
                else ""
            )
            # Create a new component
            self.new_component = self.thing_create(
                self.crosshair.thing.cpt_type,
                mouse_x,
                mouse_y,
                mouse_x + 2,
                # Have to be set to something larger because components now scale
                # to the initial size of the component.
                mouse_y,
                kind=kind,
            )
            # Clear cursors, as we dont need them when placing a cpt
            self.cursors.remove()
            return

        if self.selected:
            self.cursors.remove()
            if self.cpt_selected:  # If a component is selected
                if not self.dragged:
                    self.dragged = True
                    x0, y0 = self.select_pos
                    x0, y0 = self.snap(x0, y0)
                    self.last_pos = x0, y0
                    self.node_positions = [(node.pos.x, node.pos.y)
                                           for node in self.selected.nodes]

                # if key == "shift":
                #     if self.ui.debug:
                #         print("Separating component from circuit")
                #     old_cpt = self.selected
                #     self.selected = self.cpt_remake(self.selected)
                #     self.history.append(HistoryEvent("D", old_cpt))
                #     self.history.append(HistoryEvent("A", self.selected))
                #     self.cpt_delete(old_cpt)


                x_0, y_0 = self.last_pos
                x_1, y_1 = self.snap(mouse_x, mouse_y)
                self.last_pos = x_1, y_1

                d_x = x_1 - x_0
                d_y = y_1 - y_0

                self.cpt_move(self.selected, d_x, d_y, move_nodes=True)

            else:  # if a node is selected
                if not self.dragged:
                    self.dragged = True
                    # To save history, save first component position
                    self.node_positions = [(self.selected.pos.x, self.selected.pos.y)]

                if key == "shift":
                    if self.ui.debug:
                        print("Separating node from circuit")
                        print("node splitting is not available right now")

                self.node_move(self.selected, mouse_x, mouse_y)
        self.ui.refresh()

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
