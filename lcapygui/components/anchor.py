from .pos import Pos

class Anchor:

    def __init__(self, loc, x, y):

        self.loc = loc
        self.x = x
        self.y = y

    @property
    def xy(self):

        return self.x, self.y

    @property
    def pos(self):

        return Pos(self.x, self.y)
