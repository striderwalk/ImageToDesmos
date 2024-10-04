import numpy as np


def pairwise_distance(a, points_b):

    distances = [np.sqrt((a[0] - b0) ** 2 + (a[1] - b1) ** 2) for b0, b1 in points_b]

    return np.column_stack((points_b, distances))


def nearest_neighbor_sort(points):
    points = list(points)
    n = len(points)
    # Start from the first point
    sorted_points = [points[0]]
    points = points[1:]

    for _ in range(1, n):
        last_point = sorted_points[-1]

        distances = pairwise_distance(last_point, points)
        # Calculate distances to all other points
        min_index = np.argmin(distances[:, 1])
        nearest_point = distances[min_index, :2]
        print(nearest_point, last_point)
        sorted_points.append(nearest_point)
        points.remove(list(nearest_point))
    return np.array(sorted_points)
