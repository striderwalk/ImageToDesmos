import math

import numpy as np

from plot import plot_gradients

from .circle import is_circle
from .gradient import find_group_gradient


def to_angle(grad):
    if math.inf == grad:
        return math.pi / 2
    else:
        return math.atan2(-grad, 1)


def compare_gradients(grad1, grad2, angle):

    # Covert both gradients to angles
    theta = to_angle(grad1)
    other_theta = to_angle(grad2)

    # Check if the acutal and is less that the threshold
    return abs(theta - other_theta) > angle


def split_by_gradient(array, groups, args, angle=math.pi / 6):

    # Find the gradients in each group
    group_gradients = find_group_gradients(groups)

    for group, grad_group in group_gradients:

        for i in range(len(grad_group) - 1):

            point = grad_group[i][0]
            grad1 = grad_group[i][1]
            grad2 = grad_group[i + 1][1]

            # If the acutal and is less that the threshold
            if compare_gradients(grad1, grad2, angle):

                # Make a split at the start of the first gradients sequence
                array[point[0] : point[0] + 2, point[1] : point[1] + 2] = 0

        # For the first and last point in the group
        point1 = grad_group[0][0]
        point2 = grad_group[-1][0]

        # Skip if group is not a loop.
        if ((point1[0] + point2[0]) ** 2 + (point1[0] + point2[0]) ** 2) ** 0.5 > 10:
            continue

        grad1 = grad_group[0][1]
        grad2 = grad_group[-1][1]

        if compare_gradients(grad1, grad2, angle):

            # Make a split at the start of the first gradients sequence
            array[point1[0] : point1[0] + 2, point1[1] : point1[1] + 2] = 0

    # Display the gradients and where splits have been made
    if args.plot:
        plot_gradients(array, group_gradients)

    return array


def group_by_x(points):
    group = {}
    for y, x in points:
        if x in group:

            group[x] = group[x] + [y]
        else:
            group[x] = [y]

    return group


def find_group_gradients(groups):
    group_gradients = []

    for group in groups:
        group_gradients.append((group, find_group_gradient(group)))

    return group_gradients


def find_y_splits(array, groups):

    # Find repeated y
    for group in groups:
        x_grouped = group_by_x(group)

        if not any(len(i) > 1 for i in x_grouped.values()):
            continue

        x = sorted(x_grouped.keys())

        min_x = min(x)
        if len(x_grouped[min_x]) < 10:
            for y in x_grouped[min_x]:
                array[y, min_x : min_x + 5] = 0

        max_x = max(x)
        if len(x_grouped[max_x]) < 10:

            for y in x_grouped[max_x]:

                array[y, max_x - 5 : max_x + 1] = 0

    return array
