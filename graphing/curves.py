import json
import os
import warnings

import numpy as np
from matplotlib import pyplot as plt

from .circle import Circle
from .line import Line
from .poly import Polynomial
from .parametric import Parametric

warnings.simplefilter("ignore", np.exceptions.RankWarning)


def get_equations(size, grouped_points, mode="polynomial"):
    groups, circles, partial_circles, lines = grouped_points
    equations = []

    for group in groups:
        X = group[:, 1]
        Y = size[0] - group[:, 0]

        if mode == "polynomial":
            if np.max(Y) - np.min(Y) == 0 or np.max(X) - np.min(X) == 0:
                equations.append(Line(X, Y))

            else:
                equations.append(Polynomial(X, Y))
        elif mode == "parametric":
            equations.append(Parametric(X, Y))
        else:
            raise ValueError("Invalid mode. Use 'polynomial' or 'parametric'.")

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


def write_equations(equations, bounds, filename):
    formulas = {"bounds": {"x": bounds[0], "y": bounds[1]}}

    # Collect all the equations formatted as Latex
    for equation in equations:
        if equation.type not in formulas:
            formulas[equation.type] = []

        formulas[equation.type] = formulas[equation.type] + [equation.to_latex()]

    base = os.path.splitext(os.path.basename(filename))[0]
    with open("functions/" + base + ".equation", "w") as file:
        json.dump(formulas, file, indent=4)


def make_curves(size, grouped_points, args):

    # Get the equations
    mode = "parametric" if args.parametric else "polynomial"
    equations = get_equations(size, grouped_points, mode)

    # Save the equations to a file
    write_equations(equations, size, args.filename)

    # Plot the curves if desired
    if not args.plot:
        return
    ax = plt.gca()

    for equation in equations:
        equation.plot(ax)

    ax.set_aspect("equal")
    plt.savefig("output/graph.png")
