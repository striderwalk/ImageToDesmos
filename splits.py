import math
from gradient import find_ones
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


def find_splits(image_array, gradients, BOX_SIZE):
    edges = find_ones(image_array)
    for i in range(len(gradients)):
        for j in range(len(gradients[i])):

            if np.isnan(gradients[i, j]):
                continue

            # Orthoganals
            if i < len(gradients) - 1:
                if not np.isnan(gradients[i + 1, j]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j) * BOX_SIZE + int(BOX_SIZE / 2)
                        point = find_nearest_edge((image_i, image_j), edges)

                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if i > 0:
                if not np.isnan(gradients[i - 1, j]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j) * BOX_SIZE + int(BOX_SIZE / 2)
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i, j + 1]):
                        image_i = (i) * BOX_SIZE + int(BOX_SIZE / 2)
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if j > 0:
                if not np.isnan(gradients[i, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i, j - 1]):
                        image_i = (i) * BOX_SIZE + int(BOX_SIZE / 2)
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            # Diagonals
            if i < len(gradients) - 1 and j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i + 1, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j + 1]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if i > 0 and j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i - 1, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j + 1]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if i < len(gradients) - 1 and j > 0:
                if not np.isnan(gradients[i + 1, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j - 1]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

            if i > 0 and j > 0:
                if not np.isnan(gradients[i - 1, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j - 1]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[
                            point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                        ] = 2

    return image_array
