import numba
import numpy as np
from sklearn.cluster import DBSCAN

from .gradient import find_group_gradient
from .group_sort import nearest_neighbor_sort
from .plot import plot_groups, plot_gradients
from .splits import find_splits


@numba.jit()
def find_point_group(image_array, point):
    line = numba.typed.List()
    line.append(point)

    # Follow the line connected to points extreme[0].
    while True:
        length = len(line)
        new_line_points = numba.typed.List()
        for other in np.argwhere(image_array == 1):

            # Check for nearby neighbors.
            for point in line:

                if other is point:
                    continue

                if (point[0] - other[0]) + (point[1] - other[1]) > 2:
                    continue

                new_line_points.append((other[0], other[1]))
                image_array[other] = 0

                break

        line.extend(new_line_points)

        if len(np.argwhere(image_array == 1)) == 0:
            break
        if length == len(line):
            break
    return image_array, line


def find_point_groups(image_array):

    data = np.argwhere(image_array == 1)
    epsilon = 4
    db = DBSCAN(eps=epsilon).fit(data)
    labels = db.labels_  # labels of the found clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters
    clusters = [data[labels == i] for i in range(n_clusters)]  # list of clusters
    return clusters


def find_group_gradients(groups):
    group_gradients = []

    for group in groups:
        group_gradients.append(find_group_gradient(group))

    return group_gradients


def get_groups(image_array):
    print("pre-groups")
    groups = find_point_groups(image_array.copy())
    print("plot")
    plot_groups(groups, image_array, "groups_no_grad.png")

    # Find the gradient of edges in a BOX_SIZE x BOX_SIZE box

    print("Finding gradients.")
    groups = [nearest_neighbor_sort(group) for group in groups]
    group_gradients = find_group_gradients(groups)

    # Split the lines using the gradient
    image_array = find_splits(image_array, group_gradients)

    # Display
    print("Plotting.")
    plot_gradients(image_array, group_gradients)

    # Plot groups post-gradienting
    groups = find_point_groups(image_array.copy())

    # groups = [group for group in groups if len(group) > 10]
    plot_groups(groups, image_array)
