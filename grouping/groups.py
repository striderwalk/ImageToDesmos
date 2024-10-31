from .dbscan import find_point_groups
from plot import plot_groups
from .circle import expand_partial_circles, find_full_circles, find_partical_circles

from .lines import find_lines
from .splits import find_y_splits, split_by_gradient


def get_grouped_points(image, args):

    # Group all points.
    groups = find_point_groups(image.get_points(), args)

    # Plot the groups before splitting
    if args.plot:
        plot_groups(groups, image.array, "groups_pre_split.png")

    image.array = find_y_splits(image.array, groups)

    # Group all points.
    groups = find_point_groups(image.get_points(), args)

    # Check the mean group size
    sizes = [len(group) for group in groups]
    if sum(sizes) / len(sizes) < 20:
        print(
            "\u001b[31;1mWARNING\u001b[0m: Mean group is very low meaing image is likely poorly suited to this algorithm"
        )

    if sum(sizes) / len(sizes) > 1000:
        print(
            "\u001b[31;1mWARNING\u001b[0m: Mean group is very high meaing image may be poorly suited to this algorithm"
        )

    # Seperate out circles and sections of circles
    circles = find_full_circles(groups)

    for circle in circles:
        for point in circle:
            image.array[*point] = 0

    partial_circles = find_partical_circles(groups)
    # partial_circles = expand_partial_circles(image.get_points(), partial_circles)

    for circle in partial_circles:
        for point in circle:
            image.array[*point] = 0

    # Find lines and seperate
    image.array, line_groups = find_lines(image.array)

    # Regroup the points
    groups = find_point_groups(image.get_points(), args)

    small = [group for group in groups if len(group) < 5]
    line_groups.extend(small)
    groups = [group for group in groups if len(group) >= 5]

    # Split the point groups
    image.array = split_by_gradient(image.array, groups, args)

    # Plot groups post-splitting
    groups = find_point_groups(image.get_points(), args)

    if args.plot:
        plot_groups(groups, image.array)

    return groups, circles, partial_circles, line_groups
