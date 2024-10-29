import ast
import json
import re
import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial import polynomial, Polynomial


def convert_sci_numbers(string):

    scientific_numbers = re.findall(r"[-+]?\d*\.?\d+e[+-]\d+", string)
    for sci_num in scientific_numbers:
        normal_number = np.format_float_positional(float(sci_num))
        string = string.replace(sci_num, normal_number)
    return string


class Parametric:
    def __init__(self, x, y):
        self.type = "Parametric"
        self.x = x
        self.y = y
        self.t = np.arange(len(self.x))
        self.x_func = Polynomial(polynomial.polyfit(self.t, self.x, 5))
        self.y_func = Polynomial(polynomial.polyfit(self.t, self.y, 5))
        self.x_func.convert()
        self.y_func.convert()

    def to_latex(self):
        x_func = str(self.x_func)
        x_func = re.sub(r"\*\*(\d+)", r"^{\1}", x_func)
        x_func = x_func.replace("\n", "")
        x_func = convert_sci_numbers(x_func)
        x_func = x_func.replace("x", "t")

        y_func = str(self.y_func)
        y_func = re.sub(r"\*\*(\d+)", r"^{\1}", y_func)
        y_func = y_func.replace("\n", "")
        y_func = convert_sci_numbers(y_func)
        y_func = y_func.replace("x", "t")

        return {
            "equation": f"({x_func}, {y_func})",
            "bounds": {"min": "0", "max": str(max(self.t))},
        }
