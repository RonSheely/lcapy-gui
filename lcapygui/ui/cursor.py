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


    #     color = self.positive_colour
    #     if polarity=='negative':
    #         color = self.negative_colour
    #
    #     self.patch.append(self.sketcher.stroke_filled_circle(
    #         self.x, self.y,
    #         radius=radius,
    #         color=color,
    #         alpha=0.8
    #     ))
    #
    #     self.patch.append(self.sketcher.stroke_line(
    #         self.x - radius, self.y,
    #         self.x + radius, self.y,
    #         linewidth=2
    #     ))
    #
    #     if polarity=='positive':
    #         self.patch.append(self.sketcher.stroke_line(
    #             self.x, self.y - radius,
    #             self.x, self.y + radius,
    #             linewidth=2
    #         ))
    #
    # def remove(self):
    #     for patch in self.patch:
    #         patch.remove()