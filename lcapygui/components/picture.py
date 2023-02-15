from numpy import array, dot, sin, cos, radians


def offset(thing, offset):

    return thing.offset(offset)


def rotate(thing, angle):

    return thing.rotate(angle)


def scale(thing, scale):

    return thing.scale(scale)


class DrawingPrimitive:

    def R(self, angle):

        theta = radians(angle)
        c = cos(theta)
        s = sin(theta)
        R = array(((c, -s), (s, c)))
        return R


class Multiline(DrawingPrimitive):

    def __init__(self, *points, **kwargs):

        self.points = points
        self.kwargs = kwargs

    def __repr__(self):

        return 'Multiline' + repr(self.points)

    def offset(self, offset):

        tpoints = []
        for point in self.points:
            tpoints.append(array(point) + offset)
        return self.__class__(*tpoints, **self.kwargs)

    def scale(self, scale):

        tpoints = []
        for point in self.points:
            tpoints.append(array(point) * scale)
        return self.__class__(*tpoints, **self.kwargs)

    def rotate(self, angle):

        R = self.R(angle)

        tpoints = []
        for point in self.points:
            tpoints.append(dot(R, array(point)))
        return self.__class__(*tpoints, **self.kwargs)


class Circle(DrawingPrimitive):

    def __init__(self, centre, radius, **kwargs):

        self.centre = centre
        self.radius = radius
        self.kwargs = kwargs

    def __repr__(self):

        return 'Circle(' + repr(self.centre) + ', ' + repr(self.radius) + ')'

    def offset(self, offset):

        x = self.centre[0] + offset[0]
        y = self.centre[1] + offset[1]

        return self.__class__((x, y), self.radius, **self.kwargs)

    def scale(self, scale):

        return self.__class__(self.centre, self.radius * scale, **self.kwargs)

    def rotate(self, angle):

        R = self.R(angle)
        offset = dot(R, array(self.centre))

        return self.__class__(offset, self.radius, **self.kwargs)


class Arc(DrawingPrimitive):

    def __init__(self, centre, radius, theta1, theta2, **kwargs):

        self.centre = centre
        self.radius = radius
        self.theta1 = theta1
        self.theta2 = theta2
        self.kwargs = kwargs

    def __repr__(self):
        return 'Arc(' + repr(self.centre) + ', ' + \
            ', '.join([repr(x)
                      for x in [self.radius, self.theta1, self.theta2]]) + ')'

    def offset(self, offset):

        x = self.centre[0] + offset[0]
        y = self.centre[1] + offset[1]

        return self.__class__((x, y), self.radius,
                              self.theta1, self.theta2, **self.kwargs)

    def scale(self, scale):

        return self.__class__(self.centre, self.radius * scale,
                              self.theta1, self.theta2, **self.kwargs)

    def rotate(self, angle):

        R = self.R(angle)
        offset = dot(R, self.centre)

        return self.__class__(offset, self.radius,
                              self.theta1 + angle, self.theta2 + angle,
                              **self.kwargs)


class Picture:

    def __init__(self, *things, **kwargs):

        self.things = things
        self.kwargs = kwargs

    def __repr__(self):

        args = ', '.join([repr(thing) for thing in self.things])
        return self.__class__.__name__ + '(' + args + ')'

    def offset(self, offset):

        tthings = []
        for thing in self.things:
            tthings.append(thing.offset(offset))
        return Picture(tthings)

    def scale(self, scale):

        tthings = []
        for thing in self.things:
            tthings.append(thing.scale(scale))
        return Picture(tthings)

    def rotate(self, angle):

        tthings = []
        for thing in self.things:
            tthings.append(thing.rotate(angle))
        return Picture(tthings)


# class Foo(Things):
#
#     def __init__(self):
#         super().__init__([Circle((2, 2), 3), Circle((3, 3), 2).rotate(45)])
#
#
# class Bar(Things):
#
#     def __init__(self):
#         super().__init__([Circle((2, 2), 1), Foo().offset((1, 1))])
