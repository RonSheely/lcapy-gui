class Annotation:

    def __init__(self, ui, x, y, text, ha='center', va='center', rotate=0):

        self.sketcher = ui.sketcher
        self.x = x
        self.y = y
        self.ha = ha
        self.va = va
        self.rotate = rotate
        self.text = text
        self.patch = None

    @property
    def position(self):

        return self.x, self.y

    def draw(self, **kwargs):

        self.patch = self.sketcher.text(self.x, self.y, self.text,
                                        ha=self.ha, va=self.va, **kwargs)

    def remove(self):

        if self.patch:
            self.patch.remove()

    @classmethod
    def make_label(cls, ui, pos, angle, offset, text, flip):

        rotate = 0
        x = pos.x
        y = pos.y
        angle = round(angle, 2)

        if flip:
            offset = -offset

        if angle == 0:
            # Right
            y -= offset
            halign = 'center'
            valign = 'bottom' if flip else 'top'
        elif angle in (90, -270):
            # Up
            x += offset
            halign = 'right' if flip else 'left'
            valign = 'center'
        elif angle in (180, -180):
            # Left
            y += offset
            halign = 'center'
            valign = 'top' if flip else 'bottom'
        elif angle in (270, -90):
            # Down
            x -= offset
            halign = 'left' if flip else 'right'
            valign = 'center'
        else:
            # Rotated, TODO
            rotate = angle
            halign = 'center'
            valign = 'center'

        return cls(ui, x, y, text, halign, valign, rotate)
