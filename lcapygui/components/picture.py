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

        return 'Multiline' + str(self.points)

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
            tpoints.append(dot(R, point))
        return self.__class__(*tpoints, **self.kwargs)


class Circle(DrawingPrimitive):

    def __init__(self, offset, radius, **kwargs):

        self.offset = offset
        self.radius = radius
        self.kwargs = kwargs

    def __repr__(self):

        return 'Circle(' + str(self.offset) + ', ' + str(self.radius) + ')'

    def offset(self, offset):

        return self.__class__(self.offset + offset, self.radius,
                              **self.kwargs)

    def scale(self, scale):

        return self.__class__(self.offset, self.radius * scale, **self.kwargs)

    def rotate(self, angle):

        R = self.R(angle)
        offset = dot(R, self.offset)

        return self.__class__(offset, self.radius, **self.kwargs)


class Arc(DrawingPrimitive):

    def __init__(self, offset, radius, theta1, theta2, **kwargs):

        self.offset = offset
        self.radius = radius
        self.theta1 = theta1
        self.theta2 = theta2
        self.kwargs = kwargs

    def __repr__(self):
        return 'Arc(' + str(self.offset) + ', ' + \
            ', '.join([str(x)
                      for x in [self.radius, self.theta1, self.theta2]]) + ')'

    def offset(self, offset):

        return self.__class__(self.offset + offset, self.radius,
                              self.theta1, self.theta2, **self.kwargs)

    def scale(self, scale):

        return self.__class__(self.offset, self.radius * scale,
                              self.theta1, self.theta2, **self.kwargs)

    def rotate(self, angle):

        R = self.R(angle)
        offset = dot(R, self.offset)

        return self.__class__(offset, self.radius,
                              self.theta1 + angle, self.theta2 + angle,
                              **self.kwargs)


class Picture:

    def __init__(self, *things, **kwargs):

        self.things = things
        self.kwargs = kwargs
