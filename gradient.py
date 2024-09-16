import math
from typing import List, Tuple
import numba
import numpy as np
import tcod


@numba.jit()
def get_extreme(points) -> List[Tuple[int, int]]:
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

    return extreme_points


@numba.jit()
def find_ones(image_array):
    points = []
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            if image_array[i, j] != 0:
                points.append((i, j))
    return points


@numba.jit(nopython=False)
def find_gradient(image_array):
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

    if len(extreme) == 4:
        return find_parralel(image_array, extreme)

    if len(find_entrances(image_array)) > 2:
        print("WARN: MULITPLE ENTIES")
        print(extreme)
        print_image(image_array)
        return math.nan


def find_parralel(image_array, extreme) -> float:
    graph = tcod.path.SimpleGraph(cost=image_array, cardinal=1, diagonal=3)
    pathfinder = tcod.path.Pathfinder(graph)

    p1 = extreme[0]
    pathfinder.add_root(p1)

    if len(pathfinder.path_to(extreme[1])[1:].tolist()) != 0:
        # extreme[0] and extreme[1] and the same line
        pair1 = (p1, extreme[1])
        pair2 = (extreme[2], extreme[3])
    if len(pathfinder.path_to(extreme[2])[1:].tolist()) != 0:
        # extreme[0] and extreme[2] and the same line
        pair1 = (p1, extreme[2])
        pair2 = (extreme[1], extreme[3])

    if len(pathfinder.path_to(extreme[3])[1:].tolist()) != 0:
        # extreme[0] and extreme[3] and the same line
        pair1 = (p1, extreme[3])
        pair2 = (extreme[1], extreme[2])

        if pair1[0][1] - pair1[1][1] == 0:
            grad1 = math.inf
        else:
            grad1 = (pair1[0][0] - pair1[1][0]) / (pair1[0][1] - pair1[1][1])
        if pair2[0][1] - pair2[1][1] == 0:
            grad2 = math.inf
        else:
            grad2 = (pair2[0][0] - pair2[1][0]) / (pair2[0][1] - pair2[1][1])

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
