import argparse
import os
import timeit

from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

from curves import find_line, find_poly, find_circle
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


def poly_to_str(poly):
    coef = poly.coef
    string = (
        "y = "
        + f"{float(coef[0])} +"
        + "+".join(
            f"{float(coef[i])}" + "x^" + r"{" + str(i) + r"}"
            for i in range(1, poly.degree() + 1)
        )
    )
    # print(string)
    # print(poly)
    # print()
    return string


def main():

    # Load the image:
    filename, plot = process_args()

    image_array = get_image_array(filename)

    # Save the image array
    Image.fromarray(image_array * 255).convert("RGB").save("output/edges.png")

    groups, circles, lines = get_groups(image_array, plot)

    # return
    plt.clf()
    ax = plt.gca()

    curves_gen = []
    for group in groups:
        X = group[:, 1]
        Y = len(image_array) - group[:, 0]
        curves_gen.append(find_poly(X, Y))

    for circle in circles:
        X = circle[:, 1]
        Y = len(image_array) - circle[:, 0]
        curves_gen.append(find_circle(X, Y))

    for line in lines:
        X = line[:, 0]
        Y = len(image_array) - line[:, 1]

        curves_gen.append(find_line(X, Y))

    formulas = []
    for mode, vals in curves_gen:

        if mode == "poly":
            poly, dat, bounds = vals

            formula = poly_to_str(poly)

            formula += (
                r"\left\{" + f"{bounds[0]}" + r"<  x <" + f"{bounds[1]}" + r"\right\} "
            )
            formulas.append(formula)
            ax.plot(
                np.arange(bounds[0], bounds[1]), poly(np.arange(bounds[0], bounds[1]))
            )

        if mode == "circle":

            center, r = vals

            formula = f"(x - {center[0]})^2 + (y - {center[1]})^2 = {r**2}"
            formulas.append(formula)
            ax.add_patch(plt.Circle(center, r, fill=False))

        if mode == "line":

            grad, c, X, Y = vals

            formula = f"{grad}x + {c} = y {r"\left\{"} {np.min(X)} {r"<" } x {r"<" } {np.max(X)} {r"\right\} "}  {r"\left\{"} {np.min(Y)} {r"<" } y {r"<" } {np.max(Y)} {r"\right\} "}"
            formulas.append(formula)

            ax.plot(X, Y)

        if mode == "vline":

            X, Y = vals
            formula = f"x  = {X[0]} {r"\left\{"} {np.min(Y)} {r"<" } y {r"<" } {np.max(Y)} {r"\right\} "}"
            formulas.append(formula)

            ax.plot(X, Y)
        if mode == "hline":
            X, Y = vals
            formula = f"y = {Y[0]} {r"\left\{"} {np.min(X)} {r"<" } x {r"<" } {np.max(X)} {r"\right\} "}"
            formulas.append(formula)

            ax.plot(X, Y)

    with open("functions.txt", "w") as file:
        for formula in formulas:
            file.write(formula + "\n")
    ax.set_aspect("equal")

    plt.savefig("output/graph.png")


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)

    print(f"{time=}s")
