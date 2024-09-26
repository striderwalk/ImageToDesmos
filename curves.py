import numpy as np
from scipy.optimize import curve_fit


def exp(x, a, b, c):
    return a * np.exp(-b * x) + c


def linear(x, m, c):
    return x * m + c


def quad(x, a, b, c):
    return a * x**2 + b * x**1 + c


def cube(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d


def eplise(x, a, b, c, d, r):
    return (d**2 * (r**2 - ((x - a) ** 2) / b**2)) ** 0.5 + c


def circle(x, a, b, r):
    return np.sqrt(r**2 - (x - a) ** 2) + b


def euclidean_distance(p1, p2):
    return np.linalg.norm(p1 - p2)


# Function to sort points by distance
def sort_points_by_distance(points):

    # Mark all points as unvisited initially
    remaining_points = points.tolist()

    # Start with the first point in the list
    current_point = remaining_points.pop(0)
    sorted_points = [current_point]

    while remaining_points:

        # Calculate distance from current point to all remaining points
        distances = [
            euclidean_distance(np.array(current_point), np.array(p))
            for p in remaining_points
        ]

        # Find the index of the closest point
        nearest_index = np.argmin(distances)

        # Select the nearest point and move to it
        nearest_point = remaining_points.pop(nearest_index)
        sorted_points.append(nearest_point)
        current_point = nearest_point

    return np.array(sorted_points)


def find_curve(ones, points):
    from matplotlib import pyplot as plt

    points = sort_points_by_distance(points)
    x_data = points[:, 1]
    y_data = points[:, 0]

    min_intersections = 0
    function = None
    for test in [linear, quad, cube, exp, eplise, circle][::-1]:
        try:
            popt, pcov = curve_fit(test, x_data, y_data)
            intersections = count_intersections(ones, lambda x: test(x, *popt))
        except:
            print(f"Failed to fit points to {test.__name__}")
        # standard_deviation = np.sqrt(np.diag(pcov))
        #  print(f"{standard_deviation=}")

        if intersections > min_intersections:
            min_intersections = intersections
            function = lambda x: test(x, *popt)

    return function


def count_intersections(ones, func):
    eplison = 3
    return [abs(func(point[0]) - point[1]) < eplison for point in ones].count(True)
