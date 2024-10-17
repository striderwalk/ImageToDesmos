import numpy as np

from grouping import find_subgroup_gradient


def find_line(X, Y):

    if np.max(Y) - np.min(Y) == 0:
        return "hline", (X, Y)

    if np.max(X) - np.min(X) == 0:
        return "vline", (X, Y)

    grad = find_subgroup_gradient(np.column_stack((X, Y)))

    c = Y[0] - X[0] * grad

    return "line", (grad, c, X, Y)
