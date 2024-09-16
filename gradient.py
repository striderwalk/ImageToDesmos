import numpy as np


def get_extreme(points):
    extreme_points = []

    max_i = max(points, key=lambda x: x[0])[0]
    max_j = max(points, key=lambda x: x[1])[1]
    min_i = min(points, key=lambda x: x[0])[0]
    min_j = min(points, key=lambda x: x[1])[1]

    for point in points:
        if point[0] == max_i and point[1] == max_j:
            extreme_points.append(point)
        if point[0] == min_i and point[1] == min_j:
            extreme_points.append(point)

    return extreme_points


def find_grad(image_array):

    points = find_entrances(image_array)

    extreme = get_extreme(points)
    if len(extreme) == 2:

        points = extreme
    if len(points) == 2:
        try:
            grad = (points[0][0] - points[1][0]) / (points[0][1] - points[1][1])
            return grad
        except ZeroDivisionError:
            print(f"Error:{points=}")
    horizontal = 0
    vetical = 0
    for i in range(0, len(image_array) - 1):
        for j in range(0, len(image_array[0]) - 1):
            if image_array[i, j] == 0:
                continue
            if image_array[i + 1, j] != 0:
                vetical += 1

            if image_array[i, j + 1] != 0:
                horizontal += 1

            if image_array[i + 1, j + 1] != 0:
                vetical += 1
                horizontal += 1

    return vetical / (vetical + horizontal)


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


def print_image(image):
    for i in image:
        print()
        for j in i:
            if j == 1:
                print("\u001b[33;1m 1", end=" ")

            else:
                print("\u001b[31;1m 0", end=" ")

    print("\u001b[0m")


def gen_line(gradient, size=5):
    image_array = np.zeros(shape=(size, size))

    for i in range(1, len(image_array) + 1):
        if i * gradient <= size + 1:
            image_array[int((i - 1) * gradient), i - 1] = 1

    print_image(image_array)
    print(gradient)
    return image_array


if __name__ == "__main__":
    for i in range(1, 10):
        line = gen_line(2 * i / 10)
        print(f"{find_grad(line)=}")
        input()
