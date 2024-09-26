import argparse
import math
import os

import timeit

import numpy as np
from matplotlib import pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
from PIL import Image, ImageFilter

from curves import find_curve
from gradient import find_box_gradient, find_ones
from groups import find_point_groups
from splits import find_splits

BOX_SIZE = 7


def edge_detection(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def load(file_name):
    # Load the image
    image = Image.open(file_name)

    # Convert to standard size
    image = resize_image(image)

    # Format the image as grayscale
    image = image.convert("L")

    return image


def clear_outer(image_array):
    image_array[0, :] = 0
    image_array[-1, :] = 0
    image_array[:, 0] = 0
    image_array[:, -1] = 0
    return image_array


def resize_image(image):
    width, height = image.size
    new_width = min(200, width)
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    return image


def clear_array(image_array):
    return np.clip(image_array, 0, 1)


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


def plot_gradients(image_array, gradients):

    edges_positions = find_ones(image_array)
    for edge in edges_positions:
        # Show grad splits.
        if image_array[edge[0], edge[1]] == 2:
            plt.scatter(
                edge[1], len(image_array) - edge[0], color=(0, 1, 1, 1), marker=","
            )
        # Show grad normal points.
        if image_array[edge[0], edge[1]] == 1:
            plt.scatter(
                edge[1], len(image_array) - edge[0], color=(1, 1, 0, 0.5), marker=","
            )

    # Show the calculated gradient per box
    gradients = gradients[::-1]
    for i in range(0, len(gradients)):
        for j in range(0, len(gradients[i])):

            grad = gradients[i, j]
            if math.nan == grad:
                continue

            if math.inf == grad:
                theta = math.pi / 2

            else:
                theta = math.atan2(-grad, 1)

            dx = BOX_SIZE * math.cos(theta) / 2
            dy = BOX_SIZE * math.sin(theta) / 2
            plt.arrow(
                (j) * BOX_SIZE + BOX_SIZE / 2,
                (i) * BOX_SIZE + BOX_SIZE / 2,
                dx,
                dy,
                head_width=0.75,
            )

    plt.gca().set_aspect("equal")
    # plt.grid()
    # plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    # plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/gradients.png")


def plot_groups(groups, image_array, filename="groups.png"):
    plt.clf()
    for group in groups:
        c = np.random.random(4)
        for p in group:
            plt.scatter(p[1], len(image_array) - p[0], color=c, marker=",")
    plt.savefig("output/" + filename)


def find_t_points(image_array):

    subarrays = sliding_window_view(image_array, (3, 3))

    cases = {
        (1, 1): [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        (1, 2): [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0],
        ],
        (1, 0): [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        (0, 1): [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        (2, 1): [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
    }
    all_center_indices = []
    for offset, case in cases.items():
        case = np.array(case)
        matches = np.all(subarrays == case, axis=(2, 3))
        match_indices = np.argwhere(matches)
        center_indices = match_indices
        for index in center_indices:

            all_center_indices.append(index)

    return np.array(all_center_indices)


def remove_t_points(image_array):
    for t in find_t_points(image_array):
        image_array[t[0] : t[0] + 3, t[1] : t[1] + 3] = 0
    return image_array


def find_gradients(image_array):
    w = int(np.ceil(len(image_array) / BOX_SIZE))
    h = int(np.ceil(len(image_array[0]) / BOX_SIZE))

    gradients = np.full((w, h), math.nan, dtype=np.float64)

    for i in range(0, len(image_array), BOX_SIZE):
        for j in range(0, len(image_array[i]), BOX_SIZE):

            gradient = find_box_gradient(
                image_array[i : i + BOX_SIZE, j : j + BOX_SIZE]
            )
            gradients[i // BOX_SIZE, j // BOX_SIZE] = gradient

    return gradients


def main():

    # Load the image:
    filename = process_args()

    image = load(filename)

    # Dectect the edges of the image
    image_edges = edge_detection(image)

    image_edges.save("output/edges.png")

    # Convert the image to an array
    image_array = np.array(image_edges)
    image_array = clear_array(image_array)

    # Set all edges to 1 or 0 for non-edge
    image_array = np.minimum(image_array, np.ones(image_array.shape))

    # Remove all (that I can find) T points
    image = remove_t_points(image_array)

    # Plot groups pre-gradienting
    ones = find_ones(image_array)
    groups = find_point_groups(ones)
    plot_groups(groups, image_array, "groups_no_grad.png")

    # Find the gradient of edges in a BOX_SIZE x BOX_SIZE box
    gradients = find_gradients(image_array)

    # Split the lines using the gradient
    image_array = find_splits(image_array, gradients, BOX_SIZE)

    # Display
    # TODO plot_gradients(image_array, gradients)

    return
    ones = find_ones(image_array)
    groups = find_point_groups(ones)
    curves = []
    for group in groups:
        if x := find_curve(ones, group):
            curves.append(x)
    plt.clf()
    print(curves)
    X = np.arange(0, 200)
    for curve in curves:
        plt.plot(X, list(map(curve, X)))

    plt.show()


if __name__ == "__main__":  #
    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
