from .bipole import BipoleComponent


class Wire(BipoleComponent):

    type = 'W'
    args = ()
    has_value = False

    def draw(self, editor, sketcher, **kwargs):

        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y

        kwargs = self.make_kwargs(editor, **kwargs)
        sketcher.stroke_line(x1, y1, x2, y2, **kwargs)
