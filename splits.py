import math
import numpy as np


def is_perpendicular(grad1, grad2):

    epsilon = 1
    if abs(grad2) == 0:

        return np.isinf(abs(grad1))

    if abs(grad1) == 0:

        return np.isinf(grad1)

    if np.isinf(abs(grad1)):

        return abs(grad2) == 0

    if np.isinf(abs(grad2)):

        return abs(grad1) == 0

    return abs(grad1 - (-1 / grad2)) < epsilon


def find_nearest_edge(point, edges):
    min_distance = math.inf
    min_edge = None
    for edge in edges:
        distance = math.hypot(point[0] - edge[0], point[1] - edge[1])
        if distance < min_distance:
            min_distance = distance
            min_edge = edge

    if min_edge is None:
        raise ValueError("No edge found")
    return min_edge


def find_ones(image_array):
    # Find the coordinates of any one in the image array.
    points = []

    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            # check if the point is a one.
            if image_array[i, j] != 0:
                points.append([i, j])
    return points


def to_angle(grad):
    if math.inf == grad:
        return math.pi / 2
    else:
        return math.atan2(-grad, 1)


def find_splits(image_array, gradients, BOX_SIZE):
    edges = find_ones(image_array)

    for i in range(len(gradients)):
        for j in range(len(gradients[i])):

            grad = gradients[i, j]
            if np.isnan(grad):
                continue

            theta = to_angle(grad)

            new_i = i + int(1.5 * math.sin(theta))
            new_j = j + int(1.5 * math.cos(theta))

            if np.isnan(gradients[new_i, new_j]):
                continue
            other_theta = to_angle(gradients[new_i, new_j])
            if min(abs(theta - other_theta), abs(other_theta - theta)) > math.pi / 6:
                image_i = i * BOX_SIZE
                image_j = j * BOX_SIZE
                point = find_nearest_edge((image_i, image_j), edges)
                image_array[
                    point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                ] = 2
    return image_array
