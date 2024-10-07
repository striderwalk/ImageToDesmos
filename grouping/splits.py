import math

import numpy as np


def to_angle(grad):
    if math.inf == grad:
        return math.pi / 2
    else:
        return math.atan2(-grad, 1)


def find_splits(image_array, group_gradients):

    for grad_group in group_gradients:

        for i in range(len(grad_group) - 1):
            point = grad_group[i][0]
            grad1 = grad_group[i][1]
            grad2 = grad_group[i + 1][1]

            theta = to_angle(grad1)
            other_theta = to_angle(grad2)

            if min(abs(theta - other_theta), abs(other_theta - theta)) > math.pi / 6:

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

            if min(abs(theta - other_theta), abs(other_theta - theta)) > math.pi / 6:

                image_array[
                    point1[0] - 1 : point1[0] + 2, point1[1] - 1 : point1[1] + 2
                ] = 2

    return image_array
