import math
import numpy as np

from .group_sort import pairwise_distance


def is_full_circle(points, epsilon=1):
    center = np.mean(points[:, 0]), np.mean(points[:, 1])
    dis = pairwise_distance(center, points, just_distance=True)
    if not np.std(dis) < epsilon:
        return False

    return center, np.mean(dis)


def is_partial_circle(points, epsilon=0.5):
    x1, y1 = points[0, :]
    x2, y2 = points[len(points) // 2, :]
    x3, y3 = points[-1, :]

    # Find perp bisector p1, p2
    xmid = (x1 + x2) / 2
    ymid = (y1 + y2) / 2

    if ((x2 - x1)) != 0:

        m = (y2 - y1) / (x2 - x1)
    else:
        m = math.inf
    m1 = -1 / m
    c1 = ymid - m1 * xmid

    # Find perp bisector p2, p3
    xmid = (x2 + x3) / 2
    ymid = (y2 + y3) / 2

    if (x3 - x2) != 0:
        m = (y3 - y2) / (x3 - x2)

    else:
        m = math.inf
    m2 = -1 / m
    c2 = ymid - m2 * xmid

    # Find centre
    center_x = (c1 - c2) / (m2 - m1)
    center_y = center_x * m2 + c2

    # Find r
    r = np.sqrt((x1 - center_x) ** 2 + (y1 - center_y) ** 2)

    dis = pairwise_distance((center_x, center_y), points, just_distance=True)
    if not np.std(dis) < epsilon:
        return False, (center_x, center_y), r

    return (center_x, center_y), r


def is_circle(points, mode="partial"):

    if mode == "full":
        return is_full_circle(points)
    if mode == "partial":
        val = is_partial_circle(points)
        if val[0] == False:
            return False
        return val

    raise ValueError("mode must be either 'partial' or 'full'")


def get_circle(points, mode="full"):
    if mode == "full":
        center = np.mean(points[:, 0]), np.mean(points[:, 1])
        dis = np.mean(pairwise_distance(center, points, just_distance=True))
        return center, dis

    if mode == "partial":
        val = is_partial_circle(points)

        if val[0] == False:
            return val[1:]
        return val


def find_full_circles(groups):
    groups = [group.tolist() for group in groups]

    circles = [
        group
        for group in groups
        if is_circle(np.array(group), mode="full") is not False
    ]

    for circle in circles:

        groups.remove(circle)
    groups = [np.array(group) for group in groups]
    circles = [np.array(circle) for circle in circles]

    return groups, circles