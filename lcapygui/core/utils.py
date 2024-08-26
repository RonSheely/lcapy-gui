def point_in_triangle(x, y, path):

    x0 = path[0][0]
    x1 = path[1][0]
    x2 = path[2][0]
    y0 = path[0][1]
    y1 = path[1][1]
    y2 = path[2][1]

    s = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2)
    t = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)

    if ((s < 0) != (t < 0) and s != 0 and t != 0):
        return False

    d = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)

    return d == 0 or (d < 0) == (s + t <= 0)


def point_in_rectangle(x, y, path):

    x0 = path[0][0]
    x1 = path[1][0]
    y0 = path[0][1]
    y2 = path[2][1]

    # Assume rectangle
    l = abs(x1 - x0)
    h = abs(y2 - y0)

    return x > -l / 2 and x < l / 2 and y > -h / 2 and y < h / 2


def point_in_polygon(x, y, path):

    # Could use generic algorithm...

    if len(path) == 3:
        return point_in_triangle(x, y, path)
    elif len(path) == 4:
        return point_in_rectangle(x, y, path)
    else:
        raise ValueError('Cannot handle path of length ' + len(path))
