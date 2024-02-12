from lcapygui.components.picture import Picture
class Cursor:

    def __init__(self, ui, x, y):

        self.sketcher = ui.sketcher
        self.positive_colour = ui.model.preferences.color('positive')
        self.negative_colour = ui.model.preferences.color('negative')
        self.line_colour = ui.model.preferences.color('line')
        self.picture = Picture()
        self.x = x
        self.y = y

    @property
    def position(self):

        return self.x, self.y

    def draw(self, polarity='positive', radius=0.2):

        color = self.positive_colour
        if polarity == 'negative':
            color = self.negative_colour

        self.picture.add(self.sketcher.stroke_filled_circle(
            self.x, self.y,
            radius=radius,
            color=color,
            alpha=0.5
        ))

        self.picture.add(self.sketcher.stroke_line(
            self.x - radius, self.y,
            self.x + radius, self.y,
            color=self.line_colour,
            linewidth=1.5
        ))

        if polarity == 'positive':
            self.picture.add(self.sketcher.stroke_line(
                self.x, self.y - radius,
                self.x, self.y + radius,
                color=self.line_colour,
                linewidth=1.5
            ))

    def remove(self):
        if self.picture is not None:
            self.picture.remove()
