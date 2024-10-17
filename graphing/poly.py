import re

import numpy as np


def r_squared(func, X, Y):
    """
    r_squared =1 is best
    """

    # https://en.wikipedia.org/wiki/Coefficient_of_determination
    ss_res = sum((Y - func(X)) ** 2)
    ss_tot = sum((Y - np.mean(Y)) ** 2)

    return 1 - ss_res / ss_tot


def find_poly(X, Y):

    polys = [
        np.polynomial.polynomial.Polynomial(np.polynomial.polynomial.polyfit(X, Y, deg))
        for deg in range(2, 5)
    ]
    for p in polys:
        p.convert()

    # domain=(np.min(X), np.max(X)
    poly = min(polys, key=lambda func: 1 - (r_squared(func, X, Y)))
    # input(f"{np.min(X)==poly.domain[0]} {np.max(X)==poly.domain[1]}")
    return "poly", (poly, (np.min(X), np.max(X)))


def convert_sci_numbers(string):

    scientific_numbers = re.findall(r"[-+]?\d*\.?\d+e[+-]\d+", string)
    for sci_num in scientific_numbers:
        normal_number = np.format_float_positional(float(sci_num))
        string = string.replace(sci_num, normal_number)
    return string


def poly_to_tex(poly):
    string = str(poly)

    string = re.sub(r"\*\*(\d+)", r"^{\1}", string)
    string = string.replace("\n", "")
    string = convert_sci_numbers(string)

    return "y=" + string
