from .component import Component
from ..core.picture import Picture
from ..core.pos import Pos
from numpy import array, nan


class Fixed(Component):

    can_stretch = False

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        if len(self.nodes) == 0:
            return array(())

        if len(self.nodes) == 2:
            return array(((x1, y1), (x2, y2)))

        tf = self.make_tf(Pos(x1, y1), Pos(x2, y2),
                          self.pos1, self.pos2)

        coords = []
        for node_pinname in self.node_pinnames:
            if node_pinname == '':
                coords.append((nan, nan))
            else:
                coords.append(self.relative_pins[node_pinname].xy)

        positions = tf.transform(coords)

        return positions

    def draw(self, model, **kwargs):

        kwargs = self.make_kwargs(model, **kwargs)
        if 'invisible' in kwargs or 'nodraw' in kwargs or 'ignore' in kwargs:
            return

        self.picture = Picture()
        sketch = self._sketch_lookup(model)
        tf = self.tf()
        self.picture.add(sketch.draw(model, tf, **kwargs))
