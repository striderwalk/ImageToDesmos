from matplotlib import pyplot as plt
import numpy as np

from grouping import get_circle


def find_full_circle(X, Y):
    points = np.column_stack((X, Y))

    return get_circle(points, mode="full")


def find_partial_circle(X, Y):
    points = np.column_stack((X, Y))

    start = points[0]
    end = points[-1]

    center, r = get_circle(points, mode="partial")

    m = (start[1] - end[1]) / (start[0] - end[0])
    c = start[1] - m * start[0]

    # Above:
    x, y = points[3]
    if x * m + c < y:
        return (center, r, m, c, "gt")
    return (center, r, m, c, "lt")


class Circle:
    def __init__(self, X, Y, mode="full"):
        self.type = "Circle"

        self.X = X
        self.Y = Y
        self.circle_type = mode

        if self.circle_type == "full":
            self.center, self.r = find_full_circle(X, Y)

        elif self.circle_type == "partial":

            self.center, self.r, self.m, self.c, self.eq_type = find_partial_circle(
                X, Y
            )

    def to_latex(self):
        if self.circle_type == "full":

            return f"(x - {self.center[0]})^2 + (y - {self.center[1]})^2 = {self.r**2}"
        elif self.circle_type == "partial":

            formula = (
                f"(x - {self.center[0]})^2 + (y - {self.center[1]})^2 = {self.r**2}"
            )
            if self.eq_type == "gt":
                bounds = r"\left\{" + f"{self.m}x + {self.c} >= y" + r"\right\}"
            else:
                bounds = r"\left\{" + f"{self.m}x + {self.c} <= y" + r"\right\}"

            return formula + bounds

    def plot(self, ax):
        if self.circle_type == "full":

            ax.add_patch(plt.Circle(self.center, self.r, fill=False))

        elif self.circle_type == "partial":

            points = [
                (
                    self.r * np.cos(theta) + self.center[0],
                    self.r * np.sin(theta) + self.center[1],
                )
                for theta in np.linspace(0, np.pi * 2, 3000)
            ]

            if self.eq_type == "gt":
                points = [(x, y) for x, y in points if self.m * x + self.c <= y]
            else:
                points = [(x, y) for x, y in points if self.m * x + self.c >= y]
            points = np.array(points)

            ax.plot(points[:, 0], points[:, 1])
