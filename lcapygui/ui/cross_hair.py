from lcapygui.components.picture import Picture
from typing import Tuple


class CrossHair:
    def __init__(self, x, y, model, style="cross"):
        self.__x = x
        self.__y = y
        self.__style = style
        self.__model = model
        self.__picture = None

    @property
    def position(self) -> Tuple[int, int]:
        return self.__x, self.__y

    @position.setter
    def position(self, coords: Tuple[int, int]):
        self.__x = coords[0]
        self.__y = coords[1]

    @property
    def style(self) -> str:
        return self.__style

    @style.setter
    def style(self, style: str):
        self.__style = style

    def draw(self):
        """
        Draws a crosshair at the specified coordinates

        Parameters
        ==========
        model : lcapygui.ui.uimodelbase.UIModelBase or lcapygui.ui.uimodelmph.UIModelMPH or lcapygui.ui.uimodeldnd.UIModelDnD
            UI Model to draw to

        """
        sketcher = self.__model.ui.sketcher
        self.__picture = Picture()
        self.__picture.add(
            sketcher.stroke_line(self.__x, self.__y - 0.5, self.__x, self.__y + 0.5)
        )
        self.__picture.add(
            sketcher.stroke_line(self.__x - 0.5, self.__y, self.__x + 0.5, self.__y)
        )

    def undraw(self):
        """
        Undraws the crosshair

        """
        if self.__picture is not None:
            self.__picture.remove()

    def update(self, mouse_position, style=None, model=None):
        """
        Allows updating all parameters, and redraw the crosshair in one function
        Parameters
        ==========
        mouse_position : Tuple[int, int]
            Position of the mouse
        style : str
            Style of the crosshair
        model : lcapygui.ui.uimodelbase.UIModelBase or lcapygui.ui.uimodelmph.UIModelMPH or lcapygui.ui.uimodeldnd.UIModelDnD
            UI Model to draw to

        """

        # Update parameters
        self.position = mouse_position

        if style is not None:
            self.style = style

        if model is not None:
            self.__model = model

        # Redraw the component
        self.undraw()
        self.draw()
        self.__model.ui.refresh()
