from lcapygui.ui.history_event import HistoryEvent
from lcapygui.ui.uimodelmph import UIModelMPH
from astar import AStar
import random


class WireSolver(AStar):

    """
    Implementation of the python-astar package for finding a path between two points, with least turns

    Attributes
    ==========
    lines : list[list[int]]
        The list representation of the nodes in the circuit
    width : int
        The width of the circuit
    height : int
        The height of the circuit
    """

    def __init__(self, graph):
        self.lines = graph
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def heuristic_cost_estimate(self, node_A, node_B):
        """
        Computes the "least turns" distance between two nodes

        Explanation
        ===========
        Two points that are aligned on the same grid line have a distance of 1
        if not, they have a weight of near infinity, ensuring that paths in straight lines are preferred.

        Parameters
        ==========
        node_A : tuple[int, int]
            A tuple containing the x, y position of the first node
        node_B : tuple[int, int]
            A tuple containing the x, y position of the second node

        Returns
        =======
        int
            The distance between the two nodes
        """
        (x_1, y_1) = node_A
        (x_2, y_2) = node_B
        if x_1 == x_2 or y_1 == y_2:
            return 1
        else:
            return 10000

    def distance_between(self, node_1, node_2):
        """
        Computes the distance between two neighboring node.
        Since neighbouring nodes are always adjacent, this function always returns 1
        """
        return 1

    def neighbors(self, node):
        """
        Returns the neighbours of a given node, provided they are not an existing node.

        Parameters
        ==========
        node : tuple[int, int]
            A tuple containing the x, y position of the node

        Returns
        =======
        list[tuple[int, int]]
            A list of tuples containing the x, y position of the neighbouring nodes
        """
        x, y = node
        neighbours = [
            (nx, ny)
            # Get each neighbouring node
            for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
            # Check the points are within the bounds of the graph, and that they are not an existing node
            if (0 <= nx < self.width and 0 <= ny < self.height)
            and (self.lines[ny][nx] == 0)
        ]
        return neighbours


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
        self.chain_path = None

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

        if len(self.cursors) < 2 and self.chain_path is None:
            x1, y1 = self.snap_to_grid(mouse_x, mouse_y)
            if len(self.cursors) == 1:
                x1 = self.cursors[0].x
                y1 = self.cursors[0].y
                self.cursors.remove()

            self.draw_path(thing.cpt_type, x1, y1, mouse_x, mouse_y)

        else:
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

        # Snap mouse to grid
        mouse_x, mouse_y = self.snap_to_grid(mouse_x, mouse_y)

        # If placing a component without cursors
        if self.chain_path is not None:
            self.chain_path = None
        else:
            if self.ui.debug:
                print("Add node at (%s, %s)" % (mouse_x, mouse_y))
            # self.cursors.remove()  # TODO: stop clearing nodes on click when node-dragging is implemented
            # self.on_add_node(mouse_x, mouse_y)
            super().on_left_click(mouse_x, mouse_y)

    def on_right_click(self, mouse_x, mouse_y):
        """
        performs operations on right-click

        Explanation
        ===========
        This function is called when the user right-clicks on the canvas.
        If no component is selected, it will clear the cursors from the screen.
        Otherwise, it will show the selected components properties dialogue

        Parameters
        ==========
        mouse_x : float
            x position of the mouse
        mouse_y : float
            y position of the mouse

        """
        # Snap mouse to grid
        mouse_x, mouse_y = self.snap_to_grid(mouse_x, mouse_y)

        if self.chain_path is not None:
            print("Chain create disabled. Deleting")
            for cpt in self.chain_path:
                self.cpt_delete(cpt)
            self.chain_path = None

        else:
            super().on_right_click(mouse_x, mouse_y)
        self.unselect()

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
        if self.chain_path != None:
            # Get start node
            cpt = self.chain_path[0]
            x1 = cpt.nodes[0].pos.x
            x2 = cpt.nodes[0].pos.y
            type = cpt.type

            self.draw_path(type, x1, x2, mouse_x, mouse_y)

    def get_node_graph(self):
        """
        Creates a list representation of the nodes in the circuit
        TODO: Remove magic numbers for size of graph

        Returns
        ======
        graph : list[list[int]]
            Returns a List of Lists of ints of occupied nodes
            0 implies empty, 1 implies occupied
        """
        graph = [[0 for x in range(0, 36)] for y in range(0, 22)]

        # TODOL Make pathing more efficient
        # Path around existing nodes
        for n in self.circuit.nodes:
            graph[int(self.circuit.nodes[n].pos.y)][
                int(self.circuit.nodes[n].pos.x)
            ] = 1

        # Ignore nodes in chain_path
        if self.chain_path is not None:
            for cpt in self.chain_path:
                graph[int(cpt.gcpt.node1.pos.y)][int(cpt.gcpt.node1.pos.x)] = 0

        if self.ui.debug:
            print("Creating Node graph:")
            for row in graph:
                print(row)
            print()
        return graph

    def find_path(self, start_node, end_node, simplified=True):
        """
        Uses A* to find the path with least corners between two points

        Explanation
        ===========
        Uses get_node_graph() to create a list representation of the node positions in the graph,
        which is then passed to an A* path finder, tuned to find the simplest path possible (not shortest)
        This output path is then optionally simplified to remove unnecessary points between corners

        Parameters
        ==========
        start_node : tuple[int, int]
            The start node to path from
        end_node : tuple[int, int]
            End node to path to
        simplified : bool
            Whether to simplify the path or not

        Returns
        =======
        list[tuple[int, int]]
            A list of tuples containing the x, y position of the nodes in the path
        """
        # perform A* search to find the path between the nodes
        path = WireSolver(self.get_node_graph()).astar(start_node, end_node)

        # If no path could be found return none
        if path is None:
            return None

        path = list(path)

        if self.ui.debug:
            print(f"Found path {path}")

        # optionally simplify the path
        if simplified:
            path = self.simplify_path(path)
            if self.ui.debug:
                print(f"Simplified path {path}")

        return path

    def draw_path(self, cpt_type, x1, y1, x2, y2):
        """
        Draws a path on the canvas out of wires
        Parameters
        ==========
        y2
        x2
        y1
        x1
        cpt_type
        """
        # Snap nodes to grid
        x1, y1 = self.snap_to_grid(x1, y1)
        x2, y2 = self.snap_to_grid(x2, y2)

        # Find path between nodes
        path = self.find_path((x1, y1), (x2, y2))

        if path is None:
            return None

        # Initialise the chain path
        if self.chain_path is None:
            if self.ui.debug:
                print(f"Initialising Chain Path")
            self.chain_path = []

        # Shrink current chain to fit new path
        while len(self.chain_path) >= len(path) - 1:
            self.cpt_delete(self.chain_path.pop())

        # Undraw current chain
        for cpt in self.chain_path:
            if self.ui.debug:
                print(f"Undrawing {cpt}")
            cpt.gcpt.undraw()

        for i in range(1, len(path)):
            if i >= len(self.chain_path):
                print(f"Chain too small {i}, creating new wire")
                self.chain_path.append(
                    self.thing_create(
                        cpt_type,
                        path[i - 1][0],
                        path[i - 1][1],
                        path[i][0],
                        path[i][1],
                    )
                )
            else:
                print(f"updating wire {i}  {self.chain_path[i]}")
                self.cpt_modify_nodes(self.chain_path[i], path[i][0], path[i][1], path[i - 1][0], path[i - 1][1])

        # Draw new chain
        for cpt in self.chain_path:
            cpt.gcpt.draw(self)
        self.ui.refresh()
        print(self.chain_path)

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

    def simplify_path(self, path):
        simplified = [path[0]]
        for i in range(1, len(path) - 1):
            previous = path[i - 1]
            current = path[i]
            next = path[i + 1]
            if (previous[0] != current[0] or current[0] != next[0]) and (
                previous[1] != current[1] or current[1] != next[1]
            ):
                simplified.append(path[i])
        simplified.append(path[-1])

        return simplified
