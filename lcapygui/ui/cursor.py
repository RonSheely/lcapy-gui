class Cursor:

    def __init__(self, ui, x, y):

        self.sketcher = ui.sketcher
        self.patch = None
        self.x = x
        self.y = y

    @property
    def position(self):

        return self.x, self.y

    def draw(self, color='red', radius=0.3):

        self.patch = self.sketcher.stroke_filled_circle(self.x, self.y,
                                                        radius,
                                                        color=color,
                                                        alpha=0.5)

    def remove(self):

        self.patch.remove()
