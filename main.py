import argparse
import os
import timeit

from PIL import Image

import graphing
from grouping import get_groups
from host import host
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

    grouped_points = get_groups(image_array, plot)

    graphing.make_curves(image_array, grouped_points, filename=filename, plot=plot)
    if plot:
        host()


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
