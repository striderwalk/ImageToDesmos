import numpy as np

from grouping import find_subgroup_gradient


class Line:
    def __init__(self, X, Y):
        self.type = "Line"

        self.X = X
        self.Y = Y

        if np.max(Y) - np.min(Y) == 0:
            self.line_type = "hline"

        elif np.max(X) - np.min(X) == 0:
            self.line_type = "vline"
        else:
            self.line_type = "line"

            grad = find_subgroup_gradient(np.column_stack((X, Y)))

            c = Y[0] - X[0] * grad

            self.gradient = grad
            self.y_intcept = c

        self.domain = np.min(X), np.max(X)
        self.range = np.min(Y), np.max(Y)

    def to_latex(self):

        if self.line_type == "line":

            return (
                f"y= {self.gradient}x + {self.y_intcept}"
                + r"\left\{"
                + f"{self.domain[0]} "
                + f"< x <"
                + f"{self.domain[1]}"
                + r"\right\} "
                + r"\left\{"
                + f"{self.range[0]}"
                + f"< y <"
                + f"{self.range[1]}"
                + r"\right\}"
            )

        if self.line_type == "vline":

            return (
                f"x = {self.X[0]}"
                + r"\left\{"
                + f"{self.range[0]}"
                + f"< y <"
                + f"{self.range[1]}"
                + r"\right\} "
            )

        if self.line_type == "hline":

            return (
                f"y = {self.Y[0]}"
                + r"\left\{"
                + f"{self.domain[0]}"
                + f"< x <"
                + f" {self.domain[1]}"
                + r"\right\} "
            )

    def plot(self, ax):
        ax.plot(self.X, self.Y)
