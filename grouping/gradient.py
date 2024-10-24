import math
from typing import List
from matplotlib import pyplot as plt
import numba
import numpy as np


def find_group_gradient(group, grad_size=5):

    group = group[: group.shape[0] - (group.shape[0] % grad_size), :]
    groups_of_5 = group.reshape(-1, grad_size, 2)

    gradients = []
    for points in groups_of_5:

        gradients.append((points[0], find_subgroup_gradient(points)))

    return gradients


def find_subgroup_gradient(points):

    # Find the outermost points.
    extreme = get_extreme(points)

    # Two points definine a line.
    if len(extreme) == 2:

        # Prevent devision by zero.
        if extreme[0][1] - extreme[1][1] == 0:
            return math.inf

        # Return the gradient.

        return (extreme[0][0] - extreme[1][0]) / (extreme[0][1] - extreme[1][1])

    # Must be two lines and perpendicular lines should have been removed.
    if extreme.shape[0] == 4:
        return find_parralel(extreme, points)

    """
    Must be somthing like
        0 0 0 0 0
        0 0 0 0 1
        1 1 1 1*1*
        0 0 0 0 0
        0 0 0 0 0
    So *1* can be removed
    """

    if extreme.shape[0] == 3:
        p1 = extreme[0]
        p2 = extreme[1]
        p3 = extreme[2]

        # Find the points which shares a coordinate with both other points.
        if p1[0] == p2[0] and p2[1] == p3[1]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            return (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p1[0] == p3[0] and p3[1] == p2[1]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            return (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p2[0] == p1[0] and p1[1] == p3[1]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            return (p3[0] - p2[0]) / (p3[1] - p2[1])

        if p2[0] == p3[0] and p3[1] == p1[1]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            return (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p3[0] == p2[0] and p2[1] == p1[1]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            return (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p3[0] == p1[0] and p1[1] == p2[1]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            return (p3[0] - p2[0]) / (p3[1] - p2[1])

    # Warning: for cases which are currently unaccounded for.

    # https://pmt.physicsandmathstutor.com/download/Maths/A-level/Further/Statistics/Edexcel/FS2/Cheat-Sheets/Ch.1%20Linear%20Regression.pdf

    y = points[:, 0]
    x = points[:, 1]
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    n = len(x)
    sxy = np.sum(x * y) - mean_x * mean_y * n
    sxx = np.sum(x * x) - mean_x * mean_x * n
    if sxx == 0:

        # Horizontal
        if np.all(x == x[0]):
            return np.inf

        # Vertical
        if np.all(y == y[0]):

            return 0

    b = sxy / sxx
    a = mean_y - b * mean_x

    return a


# @numba.jit()
def get_extreme(points):
    # Find the outermost points in the box.
    extreme_points = []

    points = np.array(points)
    i = points[:, 0]
    j = points[:, 1]

    # Find the min and max values for the i and j coordinates.
    max_i = max(i)
    max_j = max(j)
    min_i = min(i)
    min_j = min(j)

    # For each point.
    for point in points:

        # If the point's i or j is the min or the max.
        if point[0] == max_i and point[1] == max_j:
            extreme_points.append(point)
            continue
        if point[0] == min_i and point[1] == min_j:
            extreme_points.append(point)
            continue

        if point[0] == min_i and point[1] == max_j:
            extreme_points.append(point)
            continue

        if point[0] == max_i and point[1] == min_j:
            extreme_points.append(point)
            continue

    # Convert to np array.
    new_points = np.zeros((len(extreme_points), 2), dtype=np.int64)

    for i in range(len(extreme_points)):
        new_points[i, :] = extreme_points[i]
    return new_points


@numba.jit()
def find_box_gradient(array):

    # If the box is empty.
    if np.all(array == 0):
        return math.nan

    # Process the box to find ones and remove any lone points since a line should be continuous.
    points = np.argwhere(array == 1)
    array = remove_lone_points(array, points)

    # Check that there is still enough points.
    if len(points) < 2:
        return math.nan

    # Find the outermost points.
    extreme = get_extreme(points)

    # Two points definine a line.
    if len(extreme) == 2:

        # Prevent devision by zero.
        if extreme[0][1] - extreme[1][1] == 0:
            return math.inf

        # Return the gradient.
        return (extreme[0][0] - extreme[1][0]) / (extreme[0][1] - extreme[1][1])

    # Must be two lines and perpendicular lines should have been removed.
    if extreme.shape[0] == 4:
        return find_parralel(extreme, points)

    """
    Must be somthing like
        0 0 0 0 0
        0 0 0 0 1
        1 1 1 1*1*
        0 0 0 0 0
        0 0 0 0 0
    So *1* can be removed
    """

    if extreme.shape[0] == 3:
        p1 = extreme[0]
        p2 = extreme[1]
        p3 = extreme[2]

        # Find the points which shares a coordinate with both other points.
        if p1[0] == p2[0] and p2[1] == p3[1]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            return (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p1[0] == p3[0] and p3[1] == p2[1]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            return (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p2[0] == p1[0] and p1[1] == p3[1]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            return (p3[0] - p2[0]) / (p3[1] - p2[1])

        if p2[0] == p3[0] and p3[1] == p1[1]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            return (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p3[0] == p2[0] and p2[1] == p1[1]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            return (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p3[0] == p1[0] and p1[1] == p2[1]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            return (p3[0] - p2[0]) / (p3[1] - p2[1])

    # Warning: for cases which are currently unaccounded for.
    if len(find_entrances(array)) > 2:
        # https://pmt.physicsandmathstutor.com/download/Maths/A-level/Further/Statistics/Edexcel/FS2/Cheat-Sheets/Ch.1%20Linear%20Regression.pdf

        y, x = np.where(array == 1)
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        n = len(x)
        sxy = np.sum(x * y) - mean_x * mean_y * n
        sxx = np.sum(x * x) - mean_x * mean_x * n
        if sxx == 0:

            # Horizontal
            if np.all(x == x[0]):
                return np.inf

            # Vertical
            if np.all(y == y[0]):
                return 0

        b = sxy / sxx
        a = mean_y - b * mean_x

        return a


# @numba.jit()
def find_parralel(extreme: List[List[int]], ones) -> float:

    # *Need* to use an array to make numba happy.
    # Size of 50 because it hasn't been to small yet.
    line = np.empty((50, 2))
    line[0, :] = extreme[0]

    # Follow the line connected to points extreme[0].
    while True:
        for i in range(len(line)):

            # Check for orthganal connections.
            if [line[i][0] + 1, line[i][1]] in ones:
                line[i, :] = [line[i][0] + 1, line[i][1]]

            if [line[i][0] - 1, line[i][1]] in ones:
                line[i, :] = [line[i][0] - 1, line[i][1]]

            if [line[i][0], line[i][1] + 1] in ones:
                line[i, :] = [line[i][0], line[i][1] + 1]

            if [line[i][0], line[i][1] - 1] in ones:
                line[i, :] = [line[i][0], line[i][1] - 1]

        # Find which other extreme point is in the line and thus the other line's extreme points.
        if np.any(line[:] == extreme[1]):
            p1x1, p1y1 = extreme[0]
            p1x2, p1y2 = extreme[1]

            p2x1, p2y1 = extreme[2]
            p2x2, p2y2 = extreme[3]
            break

        if np.any(line[:] == extreme[2]):
            p1x1, p1y1 = extreme[0]
            p1x2, p1y2 = extreme[2]

            p2x1, p2y1 = extreme[1]
            p2x2, p2y2 = extreme[3]
            break

        if np.any(line[:] == extreme[3]):
            p1x1, p1y1 = extreme[0]
            p1x2, p1y2 = extreme[3]

            p2x1, p2y1 = extreme[1]
            p2x2, p2y2 = extreme[2]
            break

    # Find the gradients of both lines.
    if p1x1 - p1x2 == 0:
        grad1 = math.inf
    else:
        grad1 = (p1y1 - p1y2) / (p1x1 - p1x2)

    if p2x1 - p2x2 == 0:
        grad2 = math.inf
    else:
        grad2 = (p2y1 - p2y2) / (p2x1 - p2x2)

    # Average the gradients.
    return (grad1 + grad2) / 2


@numba.jit()
def find_entrances(array):

    # Find all ones that are in an outer row or column of the box.
    points = set()

    # Rows
    for i in range(0, len(array)):
        if array[i, 0] != 0:
            points.add((i, 0))
        if array[i, -1] != 0:
            points.add((i, len(array[i]) - 1))

    # Columns
    for j in range(0, len(array[i])):
        if array[0, j] != 0:
            points.add((j, 0))

        if array[-1, j] != 0:
            points.add((j, len(array[i]) - 1))

    return list(points)


@numba.jit()
def print_array(array):

    # Print the box with nice formatting.
    print("___" * (len(array) + 1))

    for i in array:
        string = ""
        for j in i:
            if j == 1:
                string += " 1 "

            else:
                string += " _ "
        print("| " + string + " |")
    print("___" * (len(array) + 1))


@numba.jit()
def remove_lone_points(array, ones):

    for point in ones:
        has_friend = False
        for other in ones:
            if point is other:
                continue

            if (
                math.sqrt((point[0] - other[0]) ** 2 + (point[1] - other[1]) ** 2) - 1
                < 0.1
            ):
                has_friend = True
        if not has_friend:
            array[point[0], point[1]] = 0

    return array


def gen_line(gradient, size=5):
    # Generate lines of a specified gradient for testing purposes
    array = np.zeros(shape=(size, size))

    for i in range(1, len(array) + 1):
        if i * gradient <= size + 1:
            array[int((i - 1) * gradient), i - 1] = 1

    print_array(array)
    print(gradient)
    return array


if __name__ == "__main__":
    for i in range(1, 100):
        line = gen_line(2 * i / 10)
        print(f"{find_box_gradient(line)=}")
