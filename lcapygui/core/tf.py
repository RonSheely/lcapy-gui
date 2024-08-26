from numpy import array, dot, sqrt, degrees, arctan2
from matplotlib.transforms import Affine2D
from numpy.linalg import pinv


class TF(Affine2D):

    @classmethod
    def from_scale_angle_offset(cls, scale=1, angle=0, offset=(0, 0)):

        return cls().rotate_deg(angle).scale(scale).translate(*offset)

    @classmethod
    def from_points_pair(cls, xpos1, upos1, xpos2, upos2):
        """This creates a similarity transform (no skew)."""

        u0, v0 = upos1
        u1, v1 = upos2

        x0, y0 = xpos1
        x1, y1 = xpos2

        A = array(((x0, y0, 1, 0), (y0, -x0, 0, 1),
                   (x1, y1, 1, 0), (y1, -x1, 0, 1)))

        u = array((u0, v0, u1, v1))

        m = dot(pinv(A), u)

        H = array(((m[0], m[1], m[2]), (-m[1], m[0], m[3]), (0, 0, 1)))

        obj = cls.from_values(m[0], -m[1], m[1], m[0], m[2], m[3])
        # Hack since Affine2D hardwires class
        obj.__class__ = cls
        return obj

    def __repr__(self):

        return self.get_matrix().__repr__()

    def inverted(self):

        tf = super().inverted()
        # Hack since Affine2D hardwires class
        tf.__class__ = self.__class__
        return tf

    def transform(self, points):
        """Transform array, list, or dict of points."""

        if isinstance(points, dict):

            ret = {}
            for k, v in points.items():
                ret[k] = self.transform(v)
            return ret

        return super().transform(points)

    @property
    def scale_factor(self):

        values = self.to_values()
        H11 = values[0]
        H12 = values[2]
        H21 = values[1]
        H22 = values[3]

        return sqrt(abs(H11 * H22 - H12 * H21))

    @property
    def angle_deg(self):

        values = self.to_values()
        H11 = values[0]
        H12 = values[2]
        H21 = values[1]
        H22 = values[3]

        return degrees(arctan2(H12, H11))


def test():

    x0 = -1
    y0 = 3
    x1 = -1
    y1 = 4

    u0 = 0
    v0 = 2
    u1 = 0
    v1 = -2
    tf = TF.from_points_pair((x0, y0), (u0, v0), (x1, y1), (u1, v1))

    print(tf.transform((x0, y0)))
    print(tf.transform(((x0, y0), (x1, y1))))

    return tf
