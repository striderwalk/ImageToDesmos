import numpy as np


def find_point_group(ones, point):
    line = [point]

    # Follow the line connected to points extreme[0].
    while True:
        length = len(line)
        for i in range(len(line)):

            # Check for orthganal connections.
            if [line[i][0] + 1, line[i][1]] in ones:
                line.append([line[i][0] + 1, line[i][1]])

                ones.remove([line[i][0] + 1, line[i][1]])

            if [line[i][0] - 1, line[i][1]] in ones:
                line.append([line[i][0] - 1, line[i][1]])

                ones.remove([line[i][0] - 1, line[i][1]])

            if [line[i][0], line[i][1] + 1] in ones:
                line.append([line[i][0], line[i][1] + 1])

                ones.remove([line[i][0], line[i][1] + 1])

            if [line[i][0], line[i][1] - 1] in ones:
                line.append([line[i][0], line[i][1] - 1])

                ones.remove([line[i][0], line[i][1] - 1])

            if [line[i][0] + 1, line[i][1] + 1] in ones:
                line.append([line[i][0] + 1, line[i][1] + 1])

                ones.remove([line[i][0] + 1, line[i][1] + 1])

            if [line[i][0] - 1, line[i][1] - 1] in ones:
                line.append([line[i][0] - 1, line[i][1] - 1])

                ones.remove([line[i][0] - 1, line[i][1] - 1])

            if [line[i][0] - 1, line[i][1] + 1] in ones:
                line.append([line[i][0] - 1, line[i][1] + 1])

                ones.remove([line[i][0] - 1, line[i][1] + 1])

            if [line[i][0] + 1, line[i][1] - 1] in ones:
                line.append([line[i][0] + 1, line[i][1] - 1])

                ones.remove([line[i][0] + 1, line[i][1] - 1])

        if len(line) == length:
            break
    return np.array(line, dtype=np.float64)


def find_point_groups(ones):
    groups = []
    for one in ones:
        groups.append(find_point_group(ones, one))
    return groups
