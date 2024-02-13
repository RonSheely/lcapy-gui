from lcapygui.components.picture import Picture
from typing import Tuple


class CrossHair:
    def __init__(self, model, thing=None, label=None):
        self.position = 0, 0
        self.model = model
        self._thing = thing
        self.style = None
        self.label = None
        self.picture = Picture()

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    @position.setter
    def position(self, coords: Tuple[int, int]):
        self.x = coords[0]
        self.y = coords[1]

    @property
    def thing(self):
        return self._thing

    @thing.setter
    def thing(self, thing):
        self.style = None
        self._thing = thing

    def draw(self):
        """
        Draws a crosshair at the specified coordinates

        Parameters
        ==========
        model : lcapygui.ui.uimodelbase.UIModelBase or lcapygui.ui.uimodeldnd.UIModelDnD
            UI Model to draw to

        """

        scale = 1
        sketcher = self.model.ui.sketcher

        select_color = self.model.preferences.color('select')
        line_color = self.model.preferences.color('line')
        line_width = self.model.preferences.line_width * 1.5

        # Draw crosshair in default mode, if no style is specified
        if self.style is None:
        # If drawing a component, draw the component type
            if self.thing is not None:
                if self.thing.cpt_type == "W":
                    self.picture.add(
                        sketcher.stroke_filled_circle(
                            self.x, self.y, radius=0.2 * scale, color=select_color, alpha=.5
                        )
                    )
                else:
                    self.picture.add(
                        sketcher.text(
                            self.x + 0.2 * scale,
                            self.y + 0.2 * scale,
                            self.thing.cpt_type,
                            fontsize=self.model.preferences.font_size
                            * self.model.zoom_factor
                            * self.model.preferences.line_width_scale,
                            color=line_color
                        )
                    )

            # draw cursor
            self.picture.add(
                sketcher.stroke_line(
                    self.x, self.y - 0.5 * scale, self.x, self.y + 0.5 * scale, linewidth=line_width,color=line_color
                )
            )
            self.picture.add(
                sketcher.stroke_line(
                    self.x - 0.5 * scale, self.y, self.x + 0.5 * scale, self.y, linewidth=line_width,color=line_color
                )
            )

        elif self.style == "node": # If node style
            if self.thing is not None and (self.thing.cpt_type != "W"):
                self.picture.add(
                    sketcher.text(
                        self.x + 0.2 * scale,
                        self.y + 0.2 * scale,
                        self.thing.cpt_type,
                        fontsize=self.model.preferences.font_size
                                 * self.model.zoom_factor
                                 * self.model.preferences.line_width_scale,
                        color=line_color,
                        alpha=0
                    )
                )

            self.picture.add(
                sketcher.stroke_circle(
                    self.x, self.y, radius=0.2 * scale, color=line_color, linewidth=line_width, alpha=1
                )
            )

            self.picture.add(
                sketcher.stroke_filled_circle(
                    self.x, self.y, radius=0.1 * scale, color=select_color, linewidth=0, alpha=.5
                )
            )

            # draw cursor
            self.picture.add(
                sketcher.stroke_line(
                    self.x, self.y + 0.2 * scale, self.x, self.y + 0.5 * scale,  linewidth=line_width, color=line_color
                )
            )
            self.picture.add(
                sketcher.stroke_line(
                    self.x, self.y - 0.5 * scale, self.x, self.y - 0.2 * scale,  linewidth=line_width,color=line_color
                )
            )
            self.picture.add(
                sketcher.stroke_line(
                    self.x + 0.2 * scale, self.y, self.x + 0.5 * scale, self.y,  linewidth=line_width,color=line_color
                )
            )
            self.picture.add(
                sketcher.stroke_line(
                    self.x - 0.5 * scale, self.y, self.x - 0.2 * scale, self.y,  linewidth=line_width,color=line_color
                )
            )


    def undraw(self):
        """
        Undraws the crosshair

        """
        if self.picture is not None:
            self.picture.remove()

    def redraw(self):
        """
        Redraws the crosshair
        """
        self.undraw()
        self.draw()

    def update(self, position=None, style=None, thing=None, model=None):
        """
        Allows updating all parameters, and redrawing the crosshair in one function
        Parameters
        ==========
        position : Tuple[int, int] or None
            Position of the mouse
        style : str or None
            Style of the crosshair
        model : lcapygui.ui.uimodelbase.UIModelBase or lcapygui.ui.uimodeldnd.UIModelDnD or None
            UI Model to draw to

        """

        # Update parameters
        if position is not None:
            self.position = position

        self.style = style

        if thing is not None:
            self.thing = thing

        if model is not None:
            self.model = model

        # Redraw the component
        self.redraw()
        self.model.ui.refresh()
