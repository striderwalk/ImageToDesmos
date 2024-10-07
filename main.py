import argparse
import os
import timeit

import numpy as np
from PIL import Image

from grouping import get_groups
from image_processing import get_image_array

BOX_SIZE = 9


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


def main():

    # Load the image:
    filename = process_args()

    image_array = get_image_array(filename)

    # Save the image array
    Image.fromarray(image_array * 255).convert("RGB").save("output/edges.png")

    get_groups(image_array)


if __name__ == "__main__":  #

    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
