import os
import warnings

import numpy as np
from matplotlib import pyplot as plt

from .circle import Circle
from .line import Line
from .poly import Polynomial

warnings.simplefilter("ignore", np.exceptions.RankWarning)


def get_equations(size, grouped_points):
    groups, circles, partial_circles, lines = grouped_points
    equations = []
    for group in groups:

        X = group[:, 1]
        Y = size[0] - group[:, 0]
        equations.append(Polynomial(X, Y))

    for circle in circles:
        X = circle[:, 1]
        Y = size[0] - circle[:, 0]
        equations.append(Circle(X, Y, mode="full"))

    for circle in partial_circles:
        if len(circle) < 30:
            continue
        X = circle[:, 1]
        Y = size[0] - circle[:, 0]
        equations.append(Circle(X, Y, mode="partial"))

    for line in lines:
        X = line[:, 0]
        Y = size[0] - line[:, 1]
        equations.append(Line(X, Y))

    return equations


def write_equations(equations, filename):
    formulas = []

    # Collect all the equations formatted as Latex
    for equation in equations:
        formulas.append(str(equation))

    base = os.path.splitext(os.path.basename(filename))[0]
    with open("functions/" + base + ".equation", "w") as file:
        for formula in formulas:
            file.write(formula + "\n")


def make_curves(size, grouped_points, args):

    # Get the equations
    equations = get_equations(size, grouped_points)

    # Save the equations to a file
    write_equations(equations, args.filename)

    # Plot the curves if desired
    if not args.plot:
        return
    ax = plt.gca()

    for equation in equations:
        equation.plot(ax)

    ax.set_aspect("equal")
    plt.savefig("output/graph.png")
