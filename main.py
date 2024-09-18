import argparse
import math
import os
import random
import timeit
from math import cos, sin

import numba
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFilter

from gradient import find_gradient, find_ones


def find_edges(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def load(file_name):
    image = Image.open(file_name)

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


def plot_gradients(image_array, edges, gradients, BOX_SIZE):
    ones = find_ones(image_array)

    for one in ones:
        plt.scatter(one[1], len(image_array) - one[0], color=(1, 1, 0, 0.5), marker=".")
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
                head_width=0.5,
            )

    print("Arrows done!")

    edges.show()
    plt.gca().set_aspect("equal")
    plt.grid()
    plt.xticks(np.arange(0, len(image_array[0]) + BOX_SIZE, BOX_SIZE))
    plt.yticks(np.arange(0, len(image_array) + BOX_SIZE, BOX_SIZE))
    # plt.show()
    plt.savefig("out.png")


def main():

    # Load the image:
    filename = process_args()

    image = load(filename)

    image = resize_image(image)
    image_grayscale = image.convert("L")

    edges = find_edges(image_grayscale)
    image_array = np.array(edges)
    image_array = clear_array(image_array)

    BOX_SIZE = 5

    w = int(np.ceil(len(image_array) / BOX_SIZE))
    h = int(np.ceil(len(image_array[0]) / BOX_SIZE))

    gradients = np.full((w, h), math.nan, dtype=np.float64)
    for i in range(0, len(image_array), BOX_SIZE):
        for j in range(0, len(image_array[i]), BOX_SIZE):

            gradient = find_gradient(image_array[i : i + BOX_SIZE, j : j + BOX_SIZE])
            gradients[i // BOX_SIZE, j // BOX_SIZE] = gradient

    # Display
    plot_gradients(image_array, edges, gradients, BOX_SIZE)


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)
    print(time)
