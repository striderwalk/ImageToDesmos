import math
from typing import List, Tuple
import numba
import numpy as np
import tcod


@numba.jit()
def get_extreme(points):
    extreme_points = []

    points = np.array(points)
    i = points[:, 0]
    j = points[:, 1]

    # hi
    max_i = max(i)
    max_j = max(j)
    min_i = min(i)
    min_j = min(j)

    for point in points:

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

    new_points = np.zeros((len(extreme_points), 2), dtype=np.int64)

    for i in range(len(extreme_points)):
        new_points[i, :] = extreme_points[i]
    return new_points


@numba.jit()
def find_ones(image_array):
    points = []
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            if image_array[i, j] != 0:
                points.append([i, j])
    return points


@numba.jit()
def find_gradient(image_array):
    if np.all(image_array == 0):
        return math.nan
    points = find_ones(image_array)
    image_array = remove_lone_points(image_array, points)

    if len(points) < 2:
        return math.nan
    extreme = get_extreme(points)

    if len(extreme) == 2:

        if extreme[0][1] - extreme[1][1] == 0:
            return math.inf
        grad = (extreme[0][0] - extreme[1][0]) / (extreme[0][1] - extreme[1][1])

        return grad

    if extreme.shape[0] == 4:
        return find_parralel(extreme, points)
    if extreme.shape[0] == 3:
        p1 = extreme[0]
        p2 = extreme[1]
        p3 = extreme[2]

        if p1[0] == p2[0] and p2[1] == p3[0]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            grad = (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p1[0] == p3[0] and p3[1] == p2[0]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            grad = (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p2[0] == p1[0] and p1[1] == p3[0]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            grad = (p3[0] - p2[0]) / (p3[1] - p2[1])

        if p2[0] == p3[0] and p3[1] == p1[0]:
            if (p1[1] - p2[1]) == 0:
                return math.inf
            grad = (p1[0] - p2[0]) / (p1[1] - p2[1])

        if p3[0] == p2[0] and p2[1] == p1[0]:
            if (p1[1] - p3[1]) == 0:
                return math.inf
            grad = (p1[0] - p3[0]) / (p1[1] - p3[1])

        if p3[0] == p1[0] and p1[1] == p2[0]:
            if (p3[1] - p2[1]) == 0:
                return math.inf
            grad = (p3[0] - p2[0]) / (p3[1] - p2[1])
        return grad

    if len(find_entrances(image_array)) > 2:
        print("WARN: MULITPLE ENTIES")
        print(extreme)
        print_image(image_array)
        return math.nan


@numba.jit()
def find_parralel(extreme: List[List[int]], ones) -> float:

    line = np.empty((50, 2))
    line[0, :] = extreme[0]
    index = 1
    while True:

        for i in range(len(line)):
            if [line[i][0] + 1, line[i][1]] in ones:
                line[i, :] = [line[i][0] + 1, line[i][1]]
                index += 1

            if [line[i][0] - 1, line[i][1]] in ones:
                line[i, :] = [line[i][0] - 1, line[i][1]]
                index += 1

            if [line[i][0], line[i][1] + 1] in ones:
                line[i, :] = [line[i][0], line[i][1] + 1]
                index += 1

            if [line[i][0], line[i][1] - 1] in ones:
                line[i, :] = [line[i][0], line[i][1] - 1]
                index += 1

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

    if p1x1 - p1x2 == 0:
        grad1 = math.inf
    else:
        grad1 = (p1y1 - p1y2) / (p1x1 - p1x2)

    if p2x1 - p2x2 == 0:
        grad2 = math.inf
    else:
        grad2 = (p2y1 - p2y2) / (p2x1 - p2x2)

    return (grad1 + grad2) / 2


@numba.jit()
def find_entrances(image_array):
    # count edges
    points = set()
    for i in range(0, len(image_array)):
        if image_array[i, 0] != 0:
            points.add((i, 0))
        if image_array[i, -1] != 0:
            points.add((i, len(image_array[i]) - 1))

    for j in range(0, len(image_array[i])):
        if image_array[0, j] != 0:
            points.add((j, 0))

        if image_array[-1, j] != 0:
            points.add((j, len(image_array[i]) - 1))
    return list(points)


@numba.jit()
def print_image(image_array):
    for i in image_array:
        string = ""
        for j in i:
            if j == 1:
                string += "\u001b[33;1m 1 "

            else:
                string += "\u001b[31;1m 0 "
        print(string)
    print("\u001b[0m")


def gen_line(gradient, size=5):
    image_array = np.zeros(shape=(size, size))

    for i in range(1, len(image_array) + 1):
        if i * gradient <= size + 1:
            image_array[int((i - 1) * gradient), i - 1] = 1

    print_image(image_array)
    print(gradient)
    return image_array


@numba.jit()
def remove_lone_points(image_array, ones):

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
            image_array[point[0], point[1]] = 0

    return image_array


if __name__ == "__main__":
    for i in range(1, 100):
        line = gen_line(2 * i / 10)
        input(f"{find_gradient(line)=}")
        # input()
