import cv2
from matplotlib import pyplot as plt
import numpy as np


def find_lines(image_array, epsilon=1):

    lines = []
    v_lines = find_v_lines(image_array)
    h_lines = find_h_lines(image_array)

    lines.extend(v_lines)
    lines.extend(h_lines)

    for line in v_lines:

        y = line[0]
        image_array[line[1] : line[3] + 1, y] = 3

    for line in h_lines:

        x = line[1]
        image_array[x, line[0] : line[2] + 1] = 3

    line_groups = []
    for line in lines:
        point_line = np.linspace(line[:2], line[2:], 500)
        line_groups.append(point_line)

    point_lines = []
    # cv2.HoughLinesP(
    #     (image_array == 1).astype(np.uint8),
    #     rho=1,
    #     theta=1 * np.pi / 180,
    #     threshold=20,
    #     minLineLength=15,
    #     maxLineGap=epsilon,
    # )

    base = np.zeros(image_array.shape)

    for line in point_lines:

        cv2.line(base, line[0][:2], line[0][2:], (255, 0, 0), 1)

    for line in lines:
        # input(line)
        cv2.line(base, (line[0], line[1]), (line[2], line[3]), (128, 0, 0), 1)

    plt.imsave("./output/lines.png", base)
    plt.imsave("./output/image_array.png", image_array)

    lines = []

    for line in point_lines:
        line = line[0]

        point_line = np.linspace(line[:2], line[2:], 500)

        grad = (line[3] - line[1]) / (line[2] - line[0])

        c = line[1] - line[0] * grad

        lines.append((grad, c, point_line))

    for grad, c, point_line in lines:

        for y, x in point_line:
            y = int(y)
            x = int(x)
            try:
                if image_array[y, x] == 1:

                    image_array[y, x] = 3
            except IndexError:
                continue
        line_groups.append(point_line)

    return image_array, line_groups


def find_h_lines(image_array):
    lines = []
    for i in range(len(image_array)):
        row = image_array[i, :]

        groups = []

        in_group = False
        start_j = 0

        for j in range(len(row)):
            if row[j] == 1 and not in_group:

                in_group = True
                start_j = j
            elif row[j] == 0 and in_group:

                in_group = False
                groups.append((start_j, j - 1))

        if in_group:
            groups.append((start_j, len(row) - 1))

        for group in groups:
            if group[1] - group[0] >= 10:
                lines.append((group[0], i, group[1], i))

    return lines


def find_v_lines(image_array):
    lines = []
    for i in range(len(image_array[0])):
        row = image_array[:, i]

        groups = []

        in_group = False
        start_j = 0

        for j in range(len(row)):
            if row[j] == 1 and not in_group:

                in_group = True
                start_j = j
            elif row[j] == 0 and in_group:

                in_group = False
                groups.append((start_j, j - 1))

        if in_group:
            groups.append((start_j, len(row) - 1))

        for group in groups:
            if group[1] - group[0] >= 10:
                lines.append((i, group[0], i, group[1]))

    return lines