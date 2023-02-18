from typing import Union

from .component import Component


class Port(Component):
    """
    Port
    """

    TYPE = "P"
    NAME = "Port"

    def __init__(self):

        super().__init__(None)

    def draw(self, editor, layer):

        pass
