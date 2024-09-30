import argparse
import math
import os
import timeit

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter

from edge_dection import find_edges
from groups import find_point_groups
from gradient import find_box_gradient
from splits import find_splits
from t_junctions import remove_crosses, remove_t_points


BOX_SIZE = 4


def edge_detection(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def get_image_array(file_name):
    # Load the image.
    image = Image.open(file_name)

    image = image.quantize(16)

    image.save("output/quantize.png")

    # Format the image as grayscale.
    image = image.convert("L")

    # Convert to standard size.

    # image = image.filter(ImageFilter.CONTOUR)

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
    new_width = min(150, width)
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


def plot_gradients(image_array, gradients):
    plt.clf()

    I, J = np.where(image_array != 0)
    for edge in zip(I, J):
        # Show t splits.
        if image_array[edge[0], edge[1]] == 3:
            plt.scatter(
                edge[1], len(image_array) - edge[0], color=(1, 0, 1, 1), marker=","
            )
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
            if math.isnan(grad):
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
    plt.grid()
    plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/gradients.png")


def plot_groups(groups, image_array, filename="groups.png"):
    plt.clf()
    for group in groups:
        c = np.random.random(3)
        for p in group:
            plt.scatter(p[1], len(image_array) - p[0], color=c, marker=",")

    plt.gca().set_aspect("equal")
    # plt.grid()
    # plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    # plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    plt.savefig("output/" + filename)


def find_gradients(image_array):
    w = int(np.ceil(len(image_array) / BOX_SIZE))
    h = int(np.ceil(len(image_array[0]) / BOX_SIZE))

    gradients = np.full((w, h), math.nan, dtype=np.float64)

    for i in range(0, len(image_array), BOX_SIZE):
        for j in range(0, len(image_array[i]), BOX_SIZE):

            box = image_array[i : i + BOX_SIZE, j : j + BOX_SIZE]
            gradient = find_box_gradient(box)
            gradients[i // BOX_SIZE, j // BOX_SIZE] = gradient

    return gradients


def find_ones(image_array):
    # Find the coordinates of any one in the image array.
    points = []

    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            # check if the point is a one.
            if image_array[i, j] == 1:
                points.append([i, j])
    return points


def main():

    # Load the image:
    filename = process_args()

    image_array = get_image_array(filename)

    # Remove all (that I can find) T points
    image_array = remove_crosses(image_array)
    image_array = remove_t_points(image_array)

    print(f"{image_array=}")
    # Save the image array
    Image.fromarray(image_array * 255).convert("RGB").save("output/array.png")

    # Plot groups pre-gradienting
    print("pre-groups")
    ones = find_ones(image_array)
    groups = find_point_groups(ones)
    print("plot")
    plot_groups(groups, image_array, "groups_no_grad.png")
    print("Start", list(image_array.ravel()).count(1))

    # Find the gradient of edges in a BOX_SIZE x BOX_SIZE box

    print("Finding gradients.")
    gradients = find_gradients(image_array)

    # Split the lines using the gradient
    image_array = find_splits(image_array, gradients, BOX_SIZE)

    # Display

    print("Plotting.")
    plot_gradients(image_array, gradients)
    print("End", list(image_array.ravel()).count(1))

    # Plot groups post-gradienting
    ones = find_ones(image_array)
    groups = find_point_groups(ones)
    groups = [group for group in groups if len(group) > 10]
    plot_groups(groups, image_array)


if __name__ == "__main__":  #
    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
