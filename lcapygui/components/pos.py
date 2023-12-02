from math import sqrt


class Pos(object):

    def __init__(self, x, y=0):

        from numpy import ndarray

        if isinstance(x, tuple):
            x, y = x
        elif isinstance(x, ndarray):
            x, y = x[0], x[1]

        self.x = x
        self.y = y

    def __mul__(self, scale):

        return Pos(self.x * scale, self.y * scale)

    def __truediv__(self, scale):

        return Pos(self.x / scale, self.y / scale)

    def __add__(self, arg):

        if not isinstance(arg, Pos):
            raise ValueError('%s not a Pos' % arg)

        return Pos(self.x + arg.x, self.y + arg.y)

    def __sub__(self, arg):

        if not isinstance(arg, Pos):
            arg = Pos(arg)

        return Pos(self.x - arg.x, self.y - arg.y)

    def __str__(self):

        xstr = ('%.3f' % self.x).rstrip('0').rstrip('.')
        ystr = ('%.3f' % self.y).rstrip('0').rstrip('.')

        return "%s,%s" % (xstr, ystr)

    def __repr__(self):

        return 'Pos(%s)' % self

    @property
    def xy(self):

        from numpy import array

        return array((self.x, self.y))

    def norm(self):

        return sqrt(self.x**2 + self.y**2)
