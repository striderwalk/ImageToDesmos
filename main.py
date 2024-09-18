import argparse
import math
import os
import random
import timeit
from math import cos, sin

import numba
from numpy.lib.stride_tricks import sliding_window_view
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFilter

from gradient import find_gradient, find_ones

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

        if image_array[edge[0], edge[1]] == 2:

            plt.scatter(
                edge[1], len(image_array) - edge[0], color=(0, 1, 1, 1), marker="o"
            )
        if image_array[edge[0], edge[1]] == 1:

            plt.scatter(
                edge[1], len(image_array) - edge[0], color=(1, 1, 0, 0.5), marker="."
            )

    print("Scatter done!")
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

    print("Arrows done!")

    plt.gca().set_aspect("equal")
    plt.grid()
    plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("out.png")


def is_perpendicular(grad1, grad2):

    epsilon = 1
    if abs(grad2) == 0:

        return np.isinf(abs(grad1))

    if abs(grad1) == 0:

        return np.isinf(grad1)

    if np.isinf(abs(grad1)):

        return abs(grad2) == 0

    if np.isinf(abs(grad2)):

        return abs(grad1) == 0

    # print(grad1, grad2, abs(grad1 - (-1 / grad2)) < epsilon)
    return abs(grad1 - (-1 / grad2)) < epsilon


def find_nearest_edge(point, edges):
    min_distance = math.inf
    min_edge = None
    for edge in edges:
        distance = math.hypot(point[0] - edge[0], point[1] - edge[1])
        if distance < min_distance:
            min_distance = distance
            min_edge = edge

    if min_edge is None:
        raise ValueError("No edge found")
    return min_edge


def find_splits(image_array, gradients):
    edges = find_ones(image_array)
    for i in range(len(gradients)):
        for j in range(len(gradients[i])):

            if np.isnan(gradients[i, j]):
                continue

            # Orthoganals
            if i < len(gradients) - 1:
                if not np.isnan(gradients[i + 1, j]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j) * BOX_SIZE + int(BOX_SIZE / 2)
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if i > 0:
                if not np.isnan(gradients[i - 1, j]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j) * BOX_SIZE + int(BOX_SIZE / 2)
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i, j + 1]):
                        image_i = (i) * BOX_SIZE + int(BOX_SIZE / 2)
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if j > 0:
                if not np.isnan(gradients[i, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i, j - 1]):
                        image_i = (i) * BOX_SIZE + int(BOX_SIZE / 2)
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            # Diagonals
            if i < len(gradients) - 1 and j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i + 1, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j + 1]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if i > 0 and j < len(gradients[0]) - 1:
                if not np.isnan(gradients[i - 1, j + 1]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j + 1]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j + 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if i < len(gradients) - 1 and j > 0:
                if not np.isnan(gradients[i + 1, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i + 1, j - 1]):
                        image_i = (i + 1) * BOX_SIZE
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

            if i > 0 and j > 0:
                if not np.isnan(gradients[i - 1, j - 1]):

                    if is_perpendicular(gradients[i, j], gradients[i - 1, j - 1]):
                        image_i = (i - 1) * BOX_SIZE
                        image_j = (j - 1) * BOX_SIZE
                        point = find_nearest_edge((image_i, image_j), edges)
                        image_array[*point] = 2
                        # print("hi")

    return image_array


def find_t_points(image_array):

    subarrays = sliding_window_view(image_array, (3, 3))

    cases = [
        np.array(
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]
        ),
    ]
    all_center_indices = []
    for case in cases:
        matches = np.all(subarrays == case, axis=(2, 3))
        match_indices = np.argwhere(matches)
        center_indices = match_indices + 1
        for index in center_indices:
            all_center_indices.append(index)

    return np.array(all_center_indices)


def remove_t_points(image_array):
    for t in find_t_points(image_array):
        image_array[t[0], t[1]] = 0
    return image_array


def find_gradients(image_array):
    w = int(np.ceil(len(image_array) / BOX_SIZE))
    h = int(np.ceil(len(image_array[0]) / BOX_SIZE))

    gradients = np.full((w, h), math.nan, dtype=np.float64)

    for i in range(0, len(image_array), BOX_SIZE):
        for j in range(0, len(image_array[i]), BOX_SIZE):

            gradient = find_gradient(image_array[i : i + BOX_SIZE, j : j + BOX_SIZE])
            gradients[i // BOX_SIZE, j // BOX_SIZE] = gradient

    return gradients


def main():

    # Load the image:
    filename = process_args()

    image = load(filename)

    # Dectect the edges of the image
    image_edges = edge_detection(image)
    # Convert the image to an array
    image_array = np.array(image_edges)
    image_array = clear_array(image_array)

    # Set all edges to 1 or 0 for non-edge
    image_array = np.minimum(image_array, np.ones(image_array.shape))

    # Remove all (that I can find) T points
    image = remove_t_points(image_array)

    # Find the gradient of edges in a BOX_SIZE x BOX_SIZE box
    gradients = find_gradients(image_array)

    # Split the lines using the gradient
    image_array = find_splits(image_array, gradients)

    # Display
    plot_gradients(image_array, gradients)


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)
    print(time)
