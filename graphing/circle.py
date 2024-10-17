import numpy as np

from grouping import get_circle, nearest_neighbor_sort


def find_full_circle(X, Y):
    points = np.column_stack((X, Y))

    return "circle", get_circle(points, mode="full")


def find_partial_circle(X, Y):
    points = np.column_stack((X, Y))

    start = points[0]
    end = points[-1]

    center, r = get_circle(points, mode="partial")

    m = (start[1] - end[1]) / (start[0] - end[0])
    c = start[1] - m * start[0]

    # Above:
    x, y = points[3]
    if x * m + c < y:
        return "p_circle", (center, r, m, c, "gt")
    return "p_circle", (center, r, m, c, "lt")
