import argparse
import math
import os
import timeit

import numpy as np
from matplotlib import pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
from PIL import Image, ImageFilter

from edge_dection import find_edges
from gradient import find_box_gradient, find_group_gradient
from group_sort import nearest_neighbor_sort
from groups import find_point_groups
from splits import find_splits
from t_junctions import remove_crosses, remove_t_points

BOX_SIZE = 9


def edge_detection(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def get_image_array(file_name):
    # Load the image.
    image = Image.open(file_name)

    image = image.quantize(4)

    image.save("output/quantize.png")

    # Format the image as grayscale.
    image = image.convert("L")

    # Convert to standard size.
    image = resize_image(image)

    # Convert to np array.
    image_array = np.array(image)

    # Find the edges.
    image_array = find_edges(image_array)

    # Remove  outer edges.
    image_array = np.delete(image_array, 0, axis=0)
    image_array = np.delete(image_array, 1, axis=0)

    image_array = np.delete(image_array, -1, axis=0)
    image_array = np.delete(image_array, -2, axis=0)
    image_array = np.delete(image_array, 0, axis=1)
    image_array = np.delete(image_array, 1, axis=1)

    image_array = np.delete(image_array, -1, axis=1)
    image_array = np.delete(image_array, -2, axis=1)
    # Trim the black edges.
    # image_array = trim_array(image_array)

    return image_array


def clear_outer(image_array):
    image_array[0, :] = 0
    image_array[-1, :] = 0
    image_array[:, 0] = 0
    image_array[:, -1] = 0
    return image_array


def resize_image(image):

    width, height = image.size
    new_width = min(600, width)
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)

    return image


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str, help="Please specify a file in the CWD to convert"
    )
    args = parser.parse_args()
    if args.filename and os.path.exists(args.filename):
        filename = args.filename
    else:
        print("Please specify a file in the CWD to convert")
        exit()

    return filename


def trim_array(image_array):

    for i in range(0, len(image_array)):
        if np.all(image_array[i, :] == 0):
            image_array = np.delete(image_array, i, axis=0)
        else:
            break

    for i in range(len(image_array) - 1, -1, -1):
        if np.all(image_array[i, :] == 0):
            image_array = np.delete(image_array, i, axis=0)
        else:
            break

    for j in range(0, len(image_array[0])):
        if np.all(image_array[:, j] == 0):
            image_array = np.delete(image_array, j, axis=1)
        else:
            break

    for j in range(len(image_array) - 1, -1, -1):
        if np.all(image_array[:, j] == 0):
            image_array = np.delete(image_array, j, axis=1)
        else:
            break
    return image_array


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

            dx = (math.cos(theta) / 2) * BOX_SIZE
            dy = (math.sin(theta) / 2) * BOX_SIZE
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


# def find_gradients(image_array):
#     w = int(np.ceil(len(image_array) / BOX_SIZE))
#     h = int(np.ceil(len(image_array[0]) / BOX_SIZE))

#     gradients = np.full((w, h), math.nan, dtype=np.float64)

#     for i in range(0, len(image_array), BOX_SIZE):
#         for j in range(0, len(image_array[i]), BOX_SIZE):

#             box = image_array[i : i + BOX_SIZE, j : j + BOX_SIZE]
#             gradient = find_box_gradient(box)
#             gradients[i // BOX_SIZE, j // BOX_SIZE] = gradient

#     return gradients


def find_group_gradients(groups):
    group_gradients = []

    for group in groups:
        group_gradients.append(find_group_gradient(group))

    return group_gradients


def main():

    # Load the image:
    filename = process_args()

    image_array = get_image_array(filename)

    # Remove all (that I can find) T points
    # image_array = remove_crosses(image_array)
    # image_array = remove_t_points(image_array)

    # Save the image array
    Image.fromarray(image_array * 255).convert("RGB").save("output/edges.png")

    # Plot groups pre-gradienting
    print("pre-groups")
    groups = find_point_groups(image_array.copy())
    print("plot")
    plot_groups(groups, image_array, "groups_no_grad.png")

    # Find the gradient of edges in a BOX_SIZE x BOX_SIZE box

    print("Finding gradients.")
    groups = [nearest_neighbor_sort(group) for group in groups]
    group_gradients = find_group_gradients(groups)

    # Split the lines using the gradient
    image_array = find_splits(image_array, group_gradients)

    # Display
    print("Plotting.")
    plot_gradients(image_array, group_gradients)

    # Plot groups post-gradienting
    groups = find_point_groups(image_array.copy())

    # groups = [group for group in groups if len(group) > 10]
    plot_groups(groups, image_array)


if __name__ == "__main__":  #

    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
