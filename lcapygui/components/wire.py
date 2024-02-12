from .bipole import Bipole
from .picture import Picture


class Wire(Bipole):

    type = 'W'
    args = ()
    has_value = False

    def draw(self, model, **kwargs):
        sketcher = model.ui.sketcher

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(model, **kwargs)

        self.picture = Picture()
        self.picture.add(sketcher.stroke_line(x1, y1, x2, y2, **kwargs))
