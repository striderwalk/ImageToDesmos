import numpy as np


def pairwise_distance(a, points_b, just_distance=False):
    diff = points_b - a
    distances = np.hypot(diff[:, 0], diff[:, 1])
    if just_distance:
        return distances
    return zip(points_b, distances)


def fast_sort(points):
    # Sort the points by distance from the left most point
    points = [list(point) for point in points]

    first = min(points, key=lambda x: x[1])
    points.remove(first)

    sorted_by_distance = sorted(
        points, key=lambda p: (p[0] - first[0]) ** 2 + (p[1] - first[1]) ** 2
    )

    return np.array([first] + sorted_by_distance)


def full_sort(points):
    # Sort the points by distance from the last sorted point
    # This is slower then "fast_sort" but more precise

    points = [list(point) for point in points]

    # Start from the first point
    sorted_points = [min(points, key=lambda x: x[1])]
    points.remove(sorted_points[0])

    for _ in range(1, len(points)):
        last_point = sorted_points[-1]

        # Calculate distances to all other points
        distances = pairwise_distance(np.array(last_point), np.array(points))

        # Find the nearest point
        nearest_point = min(distances, key=lambda x: x[1])[0]

        sorted_points.append(nearest_point)
        points.remove(list(nearest_point))

    return np.array(sorted_points)


def nearest_neighbor_sort(points, fast=False):
    if fast:
        return fast_sort(points)
    else:
        return full_sort(points)
