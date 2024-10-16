import numpy as np


def pairwise_distance(a, points_b, just_distance=False):
    diff = points_b - a
    distances = np.hypot(diff[:, 0], diff[:, 1])
    if just_distance:
        return distances
    return zip(points_b, distances)


def nearest_neighbor_sort(points):
    points = [list(point) for point in points]
    n = len(points)
    # Start from the first point

    sorted_points = [min(points, key=lambda x: x[1])]
    points.remove(sorted_points[0])

    for _ in range(1, n):
        last_point = sorted_points[-1]

        distances = pairwise_distance(np.array(last_point), np.array(points))
        # Calculate distances to all other points

        nearest_point = min(distances, key=lambda x: x[1])[0]

        sorted_points.append(nearest_point)

        points.remove(list(nearest_point))

    return np.array(sorted_points)
