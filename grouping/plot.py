import math
from matplotlib import pyplot as plt
import numpy as np


def plot_groups(groups, image_array, filename="groups.png"):
    print("Group Count = ", len(groups))
    plt.clf()
    for group in groups:

        c = np.random.random(3)

        plt.scatter(group[:, 1], len(image_array) - group[:, 0], color=c, s=1)

    plt.gca().set_aspect("equal")
    # plt.grid()
    # plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    # plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/" + filename)


def plot_gradients(image_array, group_gradients):
    plt.clf()

    print("Plotting edges.")
    # Show grad normal points.

    edges = np.argwhere(image_array == 1)
    plt.scatter(edges[:, 1], len(image_array) - edges[:, 0], color=(1, 1, 0, 1), s=1)

    # Show grad splits.
    edges = np.argwhere(image_array == 2)
    plt.scatter(edges[:, 1], len(image_array) - edges[:, 0], color=(0, 1, 1, 1), s=1)

    # Show t splits.
    edges = np.argwhere(image_array == 3)
    plt.scatter(edges[:, 1], len(image_array) - edges[:, 0], color=(1, 0, 0, 1), s=1)

    print("Plotting Gradient.")
    # Show the calculated gradient per box
    # gradients = gradients[::-1]
    for gradients in group_gradients:
        for point, grad in gradients[::3]:

            if math.isnan(grad):
                continue

            if math.inf == grad:
                theta = math.pi / 2

            else:
                theta = math.atan2(-grad, 1)

            dx = (math.cos(theta) / 2) * 7
            dy = (math.sin(theta) / 2) * 7
            plt.arrow(
                (point[1]),  # * BOX_SIZE + BOX_SIZE / 2,
                (len(image_array) - point[0]),  # * BOX_SIZE + BOX_SIZE / 2,
                dx,
                dy,
                head_width=2,
            )

    plt.gca().set_aspect("equal")
    # plt.grid()
    # plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    # plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/gradients.png")
