from .components.tf import TF
from .components.pos import Pos


class Annotation:

    def __init__(self, ui, x, y, text, ha='center', va='center', rotate=0):

        self.sketcher = ui.sketcher
        self.color = ui.model.preferences.color("label")
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
                                        ha=self.ha, va=self.va, color=self.color, **kwargs)

    def remove(self):

        if self.patch:
            self.patch.remove()

    @classmethod
    def make_label(cls, ui, pos, angle, scale, offset, alignment, text):

        alignments = [('center', 'top'), ('right', 'center'),
                      ('center', 'bottom'), ('left', 'center')]

        if alignment not in alignments:
            raise ValueError('Unknown alignment ' + str(alignment))
        index = alignments.index(alignment)

        rotate = 0

        tf = TF().translate(offset[0], offset[1]
                            ).rotate_deg(angle).scale(scale)

        pos += Pos(tf.transform((0, 0)))

        angle = round(angle, 2)

        if angle == 0:
            # Right
            pass
        elif angle in (90, -270):
            # Up
            alignment = alignments[(index + 3) % 4]
        elif angle in (180, -180):
            # Left
            alignment = alignments[(index + 2) % 4]
        elif angle in (270, -90):
            # Down
            alignment = alignments[(index + 1) % 4]
        else:
            # Rotated, TODO
            rotate = angle

        return cls(ui, pos.x, pos.y, text, alignment[0], alignment[1], rotate)
