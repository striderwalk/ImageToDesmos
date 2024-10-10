import argparse
import os
import timeit

from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

import curves
from grouping import get_groups, is_circle
from image_processing import get_image_array

BOX_SIZE = 9


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str, help="Please specify a file in the CWD to convert"
    )

    parser.add_argument("-p", "--plot", action="store_true", default=False)
    args = parser.parse_args()
    if args.filename and os.path.exists(args.filename):
        filename = args.filename
    else:
        print("Please specify a file in the CWD to convert")
        exit()

    return filename, args.plot


def main():

    # Load the image:
    filename, plot = process_args()

    image_array = get_image_array(filename)

    # Save the image array
    Image.fromarray(image_array * 255).convert("RGB").save("output/edges.png")

    groups = get_groups(image_array, plot)

    # return
    plt.clf()
    ax = plt.gca()

    curves_gen = []
    for group in groups:
        X = group[:, 1]
        Y = len(image_array) - group[:, 0]
        # ax.scatter(X, Y, c=np.random.rand(4), s=1)

        curves_gen.append(curves.find_curve(np.argwhere(image_array == 1), X, Y))

    for mode, vals in curves_gen:
        if mode == "poly":
            poly, dat = vals
            ax.plot(dat, poly(dat))
        if mode == "circle":

            center, r = vals

            ax.add_patch(plt.Circle(center, r, fill=False))

    ax.set_aspect("equal")

    plt.savefig("output/graph.png")

    plt.show()


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
