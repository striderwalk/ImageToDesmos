import numba
import numpy as np

from .dbscan import find_point_groups
from plot import plot_groups

from .circle import find_full_circles, find_partical_circles, expand_partial_circles
from .lines import find_lines
from .splits import find_y_splits, split_by_gradient


def get_groups(image_array, plot=False):
    raw_image = image_array.copy()

    # Group all points.

    image_array = find_y_splits(
        image_array, find_point_groups(np.argwhere(image_array == 1))
    )
    groups = find_point_groups(np.argwhere(image_array == 1))

    if plot:
        plot_groups(groups, image_array, "groups_no_grad.png")

    # Seperate out circles
    circles = find_full_circles(groups)

    for circle in circles:
        for point in circle:

            image_array[*point] = 0
    partial_circles = find_partical_circles(groups)
    # partial_circles = expand_partial_circles(raw_image, partial_circles)
    for circle in partial_circles:
        for point in circle:

            image_array[*point] = 0

    # Find lines.
    image_array[image_array == 2] = 0
    image_array, line_groups = find_lines(image_array)

    # Regroup the points
    groups = find_point_groups(np.argwhere(image_array == 1))

    small = [group for group in groups if len(group) < 5]
    line_groups.extend(small)
    groups = [group for group in groups if len(group) >= 5]

    # Split the point groups
    image_array = split_by_gradient(image_array, groups, plot=plot)

    # Plot groups post-splitting
    groups = find_point_groups(np.argwhere(image_array == 1))

    if plot:
        plot_groups(groups, image_array)

    return groups, circles, partial_circles, line_groups
