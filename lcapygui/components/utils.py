def point_in_triangle(x, y, x0, y0, x1, y1, x2, y2):

    s = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2)
    t = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)

    if ((s < 0) != (t < 0) and s != 0 and t != 0):
        return False

    d = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)

    return d == 0 or (d < 0) == (s + t <= 0)
