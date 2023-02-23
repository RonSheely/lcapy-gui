"""
Defines the components that lcapy-gui can simulate
"""

from numpy import array, dot
from numpy.linalg import norm

from typing import Union
from abc import ABC, abstractmethod
from math import sqrt, degrees, atan2


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
    can_stretch = False
    default_kind = ''
    xoffset = 0
    yoffset = 0
    schematic_kind = False
    label_offset = 0.6

    def __init__(self, value: Union[str, int, float], kind=''):

        self.name = None
        self.value: str = value
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

        if kind == '':
            kind = self.default_kind

        self.kind = kind
        self.inv_kinds = {v: k for k, v in self.kinds.items()}

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

    @property
    def sketch_key(self):

        if self.kind != '':
            return self.TYPE + '-' + self.kind
        else:
            return self.TYPE

    def draw(self, editor, layer, **kwargs):
        """
        Handles drawing specific features of components.
        """

        # Handle ports where nothing is drawn.
        if self.sketch is None:
            return

        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position

        dx = x2 - x1
        dy = y2 - y1
        r = sqrt(dx**2 + dy**2)

        # R = array(((dx, -dy), (dy, dx))) / r
        angle = degrees(atan2(dy, dx))

        # Width in cm
        s = self.sketch.width / 72 * 2.54

        p1 = array((x1, y1))
        dp = array((dx, dy)) / r * (r - s) / 2
        p1p = p1 + dp

        lw = kwargs.pop('lw', editor.preferences.lw)

        self.sketch.draw(layer.ax, offset=p1p, angle=angle, lw=lw,
                         snap=True, **kwargs)

        if self.can_stretch:
            p2 = array((x2, y2))
            p2p = p2 - dp

            layer.stroke_line(*p1, *p1p, lw=lw, **kwargs)
            layer.stroke_line(*p2p, *p2, lw=lw, **kwargs)

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
        Returns position where to place label.
        """

        pos = self.midpoint
        w = self.label_offset
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
        if not self.schematic_kind and self.kind not in (None, ''):
            parts.append(self.kind)

        if self.TYPE not in ('W', 'P', 'O') and self.value is not None:
            if self.initial_value is None and self.name != self.value:
                if self.value.isalnum():
                    parts.append(self.value)
                else:
                    parts.append('{' + self.value + '}')

        if self.initial_value is not None:
            parts.append(self.value)
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

        if self.schematic_kind and self.kind not in (None, ''):
            attr += ', kind=' + self.kind

        return ' '.join(parts) + '; ' + attr


class BipoleComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2'


class ControlledComponent(Component):

    can_stretch = True

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2 3 4'
