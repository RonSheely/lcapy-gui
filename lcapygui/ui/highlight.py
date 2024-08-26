from ..core.picture import Picture


class Highlight:

    def __init__(self, ui):

        self.ui = ui
        self.picture = None
        self.cpt = None

    def show(self, cpt):

        if cpt == self.cpt:
            self.remove()

        self.picture = Picture()

        gcpt = cpt.gcpt
        for pin in gcpt.transformed_pins:

            self.picture.add(self.ui.sketcher.stroke_filled_circle(
                pin.x, pin.y,
                radius=0.1,
                color='green' if pin.isnode else 'purple',
                alpha=0.5
            ))

        self.cpt = cpt

    def remove(self):

        if self.cpt is None:
            return

        if self.picture is not None:
            self.picture.remove()
        self.picture = None

        self.cpt = None
