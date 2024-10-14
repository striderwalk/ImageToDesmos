import numpy as np
from sklearn.cluster import DBSCAN

from .group_sort import nearest_neighbor_sort


def find_point_groups(data):
    i_min = np.min(data[:, 0])
    j_min = np.min(data[:, 1])
    i_max = np.max(data[:, 0])
    j_max = np.max(data[:, 1])

    epsilon = 3
    db = DBSCAN(eps=epsilon).fit(data)
    labels = db.labels_  # labels of the found clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters
    clusters = [data[labels == i] for i in range(n_clusters)]  # list of clusters

    # Sort each group by point to point distance.
    clusters = [nearest_neighbor_sort(group) for group in clusters]

    return clusters
