import argparse
import os
import timeit

import graphing
from grouping import get_grouped_points
from host import host
from image_processing import ImageArray


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=str,
        help="The path of the image to process",
    )
    parser.add_argument(
        "-p",
        "--plot",
        action="store_true",
        default=False,
        help="Plot different steps in the process to the output directory",
    )
    parser.add_argument(
        "-f",
        "--fast",
        action="store_true",
        default=False,
        help="Use fast mode to increase speed with a reduction in quality",
    )
    parser.add_argument(
        "--host",
        action="store_true",
        default=False,
        help="Open a desmos page with an interactive graph view",
    )

    args = parser.parse_args()
    if args.filename and os.path.exists(args.filename):
        filename = args.filename
    else:
        print("Please specify the path of an image to convert")
        exit()

    return filename, args


def main():
    # Process the command line arguments
    filename, args = process_args()
    # Load the image:
    image = ImageArray(filename)

    # Save the image array
    image.save("output/edges.png")

    # Display warnings
    if not args.fast and len(image.get_points()) > 5000:
        print(
            "\u001b[31;1mWARNING\u001b[0m: Input image has a high complexity consider using fast mode --fast"
        )
    grouped_points = get_grouped_points(image, args)
    graphing.make_curves(image.size, grouped_points, args)

    if args.host:
        host()


if __name__ == "__main__":

    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
