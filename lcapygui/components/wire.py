from .component import Component


class Wire(Component):
    """
    Wire
    """

    TYPE = 'W'
    NAME = 'Wire'
    sketch_net = 'W 1 2'

    def draw(self, editor, layer):

        start_x, start_y = self.nodes[0].position
        end_x, end_y = self.nodes[1].position

        layer.stroke_line(start_x, start_y, end_x, end_y)
