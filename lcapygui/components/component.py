"""
Defines the components that lcapy-gui can simulate
"""

from numpy import array, dot
from numpy.linalg import norm
import ipycanvas as canvas

from typing import Union
from abc import ABC, abstractmethod
from math import sqrt, degrees, atan2, pi


class Component(ABC):

    """
    Describes an lcapy-gui component.
    This is an abstract class, specific components are derived from here.

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the component.
    """

    kinds = {}

    def __init__(self, value: Union[str, int, float]):

        self.name = None
        self.value: str = value
        self.kind = None
        self.nodes = []
        self.initial_value = None
        self.control = None
        self.attrs = ''
        self.opts = []
        self.annotations = []
        self.label = ''
        self.voltage_label = ''
        self.current_label = ''
        self.angle = 0

    @property
    @classmethod
    @abstractmethod
    def TYPE(cls) -> str:
        """
        Component type identifer used by lcapy.
        E.g. Resistors have the identifier R.
        """
        ...

    @property
    @classmethod
    @abstractmethod
    def NAME(cls) -> str:
        """
        The full name of the component.
        E.g. Resistor
        """
        ...

    def __str__(self) -> str:

        return self.TYPE + ' ' + '(%s, %s) (%s, %s)' % \
            (self.nodes[0].position[0], self.nodes[0].position[1],
             self.nodes[1].position[0], self.nodes[1].position[1])

    @abstractmethod
    def draw(self, editor, layer: canvas.Canvas):
        """
        Handles drawing specific features of components.

        Component end nodes are handled by the draw method, which calls this
        abstract method.

        """
        ...

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return norm(array(self.nodes[1].position)
                    - array(self.nodes[0].position))

    @property
    def midpoint(self) -> array:
        """
        Computes the midpoint of the component.
        """

        return (array(self.nodes[0].position)
                + array(self.nodes[1].position)) / 2

    def along(self) -> array:
        """
        Computes a unit vector pointing along the line of the component.
        If the length of the component is zero, this will return the
        zero vector.
        """
        length = self.length()
        if length == 0:
            return array((0, 0))
        else:
            return (array(self.nodes[1].position)
                    - array(self.nodes[0].position))/length

    def orthog(self) -> array:
        """
        Computes a unit vector pointing anti-clockwise to the line
        of the component.
        """
        delta = self.along()

        rot = array([[0, -1],
                     [1, 0]])
        return dot(rot, delta)

    @property
    def vertical(self) -> bool:
        """
        Returns true if component essentially vertical.
        """

        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position
        return abs(y2 - y1) > abs(x2 - x1)

    @property
    def label_position(self) -> array:
        """
        Returns position where to place label.   This should be
        customised for each component.
        """

        pos = self.midpoint
        w = 0.75
        if self.vertical:
            pos[0] += w
        else:
            pos[1] += w

        return pos

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), (x2, y2)))

    def net(self, components, step=1):

        parts = [self.name]
        for node in self.nodes[0:2]:
            parts.append(node.name)

        if self.TYPE in ('E', 'F', 'G', 'H') \
           and self.control is None and self.NAME != 'Opamp':
            raise ValueError(
                'Control component not defined for ' + self.name)

        if self.TYPE in ('E', 'G'):

            if self.NAME == 'Opamp':
                parts.append('opamp')
                for node in self.nodes[2:4]:
                    parts.append(node.name)
            else:
                # Lookup nodes for the control component.
                idx = components.find_index(self.control)
                parts.append(components[idx].nodes[0].name)
                parts.append(components[idx].nodes[1].name)
        elif self.TYPE in ('F', 'H'):
            parts.append(self.control)

        # Later need to handle schematic kind attributes.
        if self.kind is not None and self.kinds[self.kind] != '':
            parts.append(self.kinds[self.kind])

        if self.TYPE not in ('W', 'P', 'O') and self.value is not None:
            if self.initial_value is None and self.name != self.value:
                if self.value.isalnum():
                    parts.append(self.value)
                else:
                    parts.append('{' + self.value + '}')

        if self.initial_value is not None:
            if self.initial_value.isalnum():
                parts.append(self.initial_value)
            else:
                parts.append('{' + self.initial_value + '}')

        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position
        r = sqrt((x1 - x2)**2 + (y1 - y2)**2) / step

        if r == 1:
            size = ''
        else:
            size = '=' + str(round(r, 2)).rstrip('0').rstrip('.')

        if y1 == y2:
            if x1 > x2:
                attr = 'left' + size
            else:
                attr = 'right' + size
        elif x1 == x2:
            if y1 > y2:
                attr = 'down' + size
            else:
                attr = 'up' + size
        else:
            angle = degrees(atan2(y2 - y1, x2 - x1))
            attr = 'rotate=' + str(round(angle, 2)).rstrip('0').rstrip('.')

        if self.TYPE == 'Eopamp':
            # TODO: fix for other orientations
            attr = 'right'

        # Add user defined attributes such as color=blue, thick, etc.
        if self.attrs != '':
            attr += ', ' + self.attrs

        return ' '.join(parts) + '; ' + attr
