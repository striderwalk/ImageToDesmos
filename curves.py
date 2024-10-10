from matplotlib import pyplot as plt
import numpy as np
from PyDesmos import Graph
from grouping import is_circle


def find_circle(X, Y, possible_points):

    x1, y1 = X[0], Y[0]
    x2, y2 = X[len(X) // 2], Y[len(X) // 2]
    x3, y3 = X[-1], Y[-1]

    # Find perp bisector p1, p2
    xmid = (x1 + x2) / 2
    ymid = (y1 + y2) / 2

    m = (y2 - y1) / (x2 - x1)

    m1 = -1 / m
    c1 = ymid - m1 * xmid

    # Find perp bisector p2, p3
    xmid = (x2 + x3) / 2
    ymid = (y2 + y3) / 2

    m = (y3 - y2) / (x3 - x2)
    m2 = -1 / m
    c2 = ymid - m2 * xmid

    # Find centre
    # c_x = (c2 - c1) / (m1 - m2)
    c_x = (c1 - c2) / (m2 - m1)
    c_y = c_x * m2 + c2

    # Find r
    r = np.sqrt((x1 - c_x) ** 2 + (y1 - c_y) ** 2)

    points = []

    for x, y in zip(X, Y):
        if (x - c_x) ** 2 + (y - c_y) ** 2 - r**2 < 5:
            # angles.append(np.atan2(y - c_y, x - c_x))

            points.append((x, y))

    if len(points) / len(X) < 60:
        return None

    all_points = []
    for x, y in possible_points:
        if (x - c_x) ** 2 + (y - c_y) ** 2 - r**2 < 5:
            # angles.append(np.atan2(y - c_y, x - c_x))

            all_points.append((x, y))
    if len(all_points) > len(points):
        return (c_x, c_y), r

    return None


def find_curve(possible_points, X, Y):
    max_r = np.max(X) - np.min(X)
    if (circle := is_circle(np.column_stack((X, Y)), mode="full")) and len(X) > 30:
        if circle[1] < max_r:

            return "circle", circle

    polys = [
        np.polynomial.polynomial.Polynomial(np.polynomial.polynomial.polyfit(X, Y, deg))
        for deg in range(1, 7)
    ]

    poly = min(polys, key=lambda func: abs(r_squared(func, X, Y) - 1))

    # dat_range = np.max(X) - np.min(X)
    # extra = int(dat_range * 0.05) if poly.degree() == 1 else 0
    # extra = 0
    # dat = np.arange(np.min(X) - extra, np.max(X) + extra, 0.6)

    dat = np.arange(np.min(X), np.max(X), 0.6)

    return "poly", (poly, dat)


def r_squared(func, X, Y):
    """
    r_squared =1 is best
    """

    # https://en.wikipedia.org/wiki/Coefficient_of_determination
    ss_res = sum((Y - func(X)) ** 2)
    ss_tot = sum((Y - np.mean(Y)) ** 2)

    return 1 - ss_res / ss_tot
