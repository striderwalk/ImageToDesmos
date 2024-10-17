import os
import warnings

import numpy as np
from matplotlib import pyplot as plt

from .circle import find_full_circle, find_partial_circle
from .line import find_line
from .poly import find_poly, poly_to_tex

warnings.simplefilter("ignore", np.exceptions.RankWarning)


def get_equations(image_array, grouped_points):
    groups, circles, partial_circles, lines = grouped_points
    curves_gen = []
    for group in groups:

        X = group[:, 1]
        Y = len(image_array) - group[:, 0]
        curves_gen.append(find_poly(X, Y))
    for circle in circles:

        X = circle[:, 1]
        Y = len(image_array) - circle[:, 0]
        curves_gen.append(find_full_circle(X, Y))
    for circle in partial_circles:
        if len(circle) < 30:
            continue
        X = circle[:, 1]
        Y = len(image_array) - circle[:, 0]
        curves_gen.append(find_partial_circle(X, Y))
    for line in lines:
        X = line[:, 0]
        Y = len(image_array) - line[:, 1]
        curves_gen.append(find_line(X, Y))

    return curves_gen


def write_equations(equations, filename):
    formulas = []
    for mode, vals in equations:

        if mode == "poly":
            poly, bounds = vals

            string = str(poly)
            string = string.replace("\n", "")
            string += f"{r"{"} {bounds[0]} < x < {bounds[1]} {r"}"}"

            formula = poly_to_tex(poly)

            formula += (
                r"\left\{" + f"{bounds[0]}" + r"< x <" + f"{bounds[1]}" + r"\right\} "
            )
            formulas.append(formula)

        if mode == "circle":

            center, r = vals

            formula = f"(x - {center[0]})^2 + (y - {center[1]})^2 = {r**2}"
            formulas.append(formula)

        if mode == "p_circle":

            center, r, m, c, sign = vals

            formula = f"(x - {center[0]})^2 + (y - {center[1]})^2 = {r**2}"
            if sign == "gt":
                bounds = f"{r"\left\{"} {m}x + {c} {r"<=" } y {r"\right\} "}"
            else:
                bounds = f"{r"\left\{"} {m}x + {c} {r">=" } y {r"\right\} "}"

            formulas.append(formula + bounds)

        if mode == "line":

            grad, c, X, Y = vals

            formula = f"{grad}x + {c} = y {r"\left\{"} {np.min(X)} {r"<" } x {r"<" } {np.max(X)} {r"\right\} "}  {r"\left\{"} {np.min(Y)} {r"<" } y {r"<" } {np.max(Y)} {r"\right\} "}"
            formulas.append(formula)

        if mode == "vline":

            X, Y = vals
            formula = f"x  = {X[0]} {r"\left\{"} {np.min(Y)} {r"<" } y {r"<" } {np.max(Y)} {r"\right\} "}"
            formulas.append(formula)

        if mode == "hline":
            X, Y = vals
            formula = f"y = {Y[0]} {r"\left\{"} {np.min(X)} {r"<" } x {r"<" } {np.max(X)} {r"\right\} "}"
            formulas.append(formula)
    base = os.path.splitext(os.path.basename(filename))[0]

    with open("functions/" + base + ".equation", "w") as file:
        for formula in formulas:
            file.write(formula + "\n")


def make_curves(image_array, grouped_points, filename="function.txt", plot=False):

    if plot:
        plt.clf()
        for points in grouped_points[1]:
            c = np.random.random(3)
            plt.scatter(points[:, 1], len(image_array) - points[:, 0], c=c)
        for points in grouped_points[2]:
            c = np.random.random(3)
            plt.scatter(points[:, 1], len(image_array) - points[:, 0], c=c)
            plt.scatter(
                points[0, 1], len(image_array) - points[0, 0], c="red", marker="x"
            )
            plt.scatter(
                points[-1, 1], len(image_array) - points[-1, 0], c="blue", marker="x"
            )

        plt.gca().set_aspect("equal")
        plt.savefig("output/circles.png")
        plt.clf()

    equations = get_equations(image_array, grouped_points)
    write_equations(equations, filename)

    if not plot:
        return
    ax = plt.gca()

    # Plot
    for mode, vals in equations:

        if mode == "poly":
            poly, bounds = vals

            X = np.linspace(bounds[0], bounds[1], 20000)
            ax.plot(X, poly(X), c="blue")

        if mode == "circle":

            center, r = vals

            ax.add_patch(plt.Circle(center, r, fill=False))

        if mode == "p_circle":

            center, r, m, c, sign = vals

            points = [
                (r * np.cos(theta) + center[0], r * np.sin(theta) + center[1])
                for theta in np.linspace(0, np.pi * 2, 3000)
            ]

            if sign == "gt":
                points = [(x, y) for x, y in points if m * x + c <= y]
            else:
                points = [(x, y) for x, y in points if m * x + c >= y]
            points = np.array(points)

            ax.plot(points[:, 0], points[:, 1])

        if mode == "line":

            grad, c, X, Y = vals

            ax.plot(X, Y)

        if mode == "vline":

            X, Y = vals

            ax.plot(X, Y)
        if mode == "hline":
            X, Y = vals

            ax.plot(X, Y)

    ax.set_aspect("equal")

    plt.savefig("output/graph.png")
