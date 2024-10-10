import numba
import numpy as np
from sklearn.cluster import DBSCAN

from .circle import find_full_circles, get_circle, is_circle

from .group_sort import nearest_neighbor_sort
from plot import plot_groups
from .splits import find_y_splits, split_by_gradient


def find_point_groups(image_array):
    data = np.argwhere(image_array == 1)
    epsilon = 3
    db = DBSCAN(eps=epsilon).fit(data)
    labels = db.labels_  # labels of the found clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters
    clusters = [data[labels == i] for i in range(n_clusters)]  # list of clusters

    # Sort each group by point to point distance.
    clusters = [nearest_neighbor_sort(group) for group in clusters]

    return clusters


def get_groups(image_array, plot=False):

    # Group all points.
    groups = find_point_groups(image_array)

    if plot:
        plot_groups(groups, image_array, "groups_no_grad.png")

    # Seperate out circles
    groups, circles = find_full_circles(groups)

    # Split the point groups
    image_array = split_by_gradient(image_array, groups, plot=plot)
    image_array = find_y_splits(image_array, groups)

    # if plot:
    # plot_groups(find_point_groups(image_array), image_array, "group_no_split.png")

    # Plot groups post-splitting
    groups = find_point_groups(image_array)

    if plot:
        plot_groups(groups, image_array)

    return groups + circles
