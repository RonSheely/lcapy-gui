class Multiline:

    def __init__(self, start, *points, **kwargs):

        self.start = start
        self.points = points
        self.kwargs = kwargs


class Circle:

    def __init__(self, centre, radius, **kwargs):

        self.centre = centre
        self.radius = radius
        self.kwargs = kwargs


class Arc:

    def __init__(self, centre, radius, theta1, theta2, **kwargs):

        self.centre = centre
        self.radius = radius
        self.theta1 = theta1
        self.theta2 = theta2
        self.kwargs = kwargs


class Picture:

    def __init__(self, *things, **kwargs):

        self.things = things
        self.kwargs = kwargs
