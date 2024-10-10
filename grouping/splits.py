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


def split_by_gradient(image_array, groups, angle=math.pi / 7, plot=False):

    group_gradients = find_group_gradients(groups)

    for group, grad_group in group_gradients:

        if is_circle(group):
            continue

        for i in range(len(grad_group) - 1):

            point = grad_group[i][0]
            grad1 = grad_group[i][1]
            grad2 = grad_group[i + 1][1]

            theta = to_angle(grad1)
            other_theta = to_angle(grad2)

            if abs(theta - other_theta) > angle:

                image_array[
                    point[0] - 1 : point[0] + 2, point[1] - 1 : point[1] + 2
                ] = 2

        # If group is a loop.
        point1 = grad_group[0][0]
        point2 = grad_group[-1][0]
        if ((point1[0] + point2[0]) ** 2 + (point1[0] + point2[0]) ** 2) ** 0.5 < 10:

            grad1 = grad_group[0][1]
            grad2 = grad_group[-1][1]

            theta = to_angle(grad1)
            other_theta = to_angle(grad2)

            if abs(theta - other_theta) > angle:

                image_array[
                    point1[0] - 1 : point1[0] + 2, point1[1] - 1 : point1[1] + 2
                ] = 2
    # Display
    if plot:
        plot_gradients(image_array, group_gradients)

    return image_array


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


def find_y_splits(image_array, groups):

    # Find repeated y
    for group in groups:
        x_grouped = group_by_x(group)
        # print(x_grouped)

        if not any(len(i) > 1 for i in x_grouped.values()):
            continue

        x = sorted(x_grouped.keys())

        min_x = min(x)
        if len(x_grouped[min_x]) < 5:
            for y in x_grouped[min_x]:
                image_array[y, min_x] = 2

        max_x = max(x)
        if len(x_grouped[max_x]) < 5:

            for y in x_grouped[max_x]:

                image_array[y, max_x] = 2

    return image_array
