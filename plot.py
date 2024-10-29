import math

import numpy as np
from matplotlib import pyplot as plt


def to_angle(grad):
    if math.inf == grad:
        return math.pi / 2
    else:
        return math.atan2(-grad, 1)


def plot_groups(groups, array, filename="groups.png"):
    plt.clf()
    ax = plt.gca()
    for group in groups:

        c = np.random.random(3)

        ax.scatter(group[:, 1], len(array) - group[:, 0], color=c, s=1)

    ax.set_aspect("equal")
    # plt.grid()
    # plt.xticks(np.arange(0, len(array[0]) + BOX_SIZE, BOX_SIZE))
    # plt.yticks(np.arange(0, len(array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/" + filename)


def plot_gradients(array, group_gradients):
    plt.clf()
    ax = plt.gca()

    # Show grad normal points.

    edges = np.argwhere(array == 1)
    ax.scatter(edges[:, 1], len(array) - edges[:, 0], color=(1, 1, 0, 1), s=1)

    # Show grad splits.
    edges = np.argwhere(array == 2)

    ax.scatter(edges[:, 1], len(array) - edges[:, 0], color=(0, 1, 1, 1), s=1)

    # Show other splits
    edges = np.argwhere(array == 3)
    ax.scatter(edges[:, 1], len(array) - edges[:, 0], color=(1, 0, 0, 1), s=1)

    # Show the calculated gradient per box
    for _, gradients in group_gradients:

        for point, grad in gradients[::3]:
            if math.isnan(grad):
                continue

            theta = to_angle(grad)

            dx = (math.cos(theta)) * 8
            dy = (math.sin(theta)) * 8
            ax.arrow(
                (point[1]),
                (len(array) - point[0]),
                dx,
                dy,
                head_width=2,
            )

    ax.set_aspect("equal")
    plt.savefig("output/gradients.png")
