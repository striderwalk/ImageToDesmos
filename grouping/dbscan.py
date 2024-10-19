import numpy as np
from sklearn.cluster import DBSCAN

from .group_sort import nearest_neighbor_sort


def find_point_groups(data, args):

    epsilon = 3
    db = DBSCAN(eps=epsilon).fit(data)
    labels = db.labels_  # labels of the found clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters
    clusters = [data[labels == i] for i in range(n_clusters)]  # list of clusters

    # Sort each group by point to point distance.
    clusters = [nearest_neighbor_sort(group, args.fast) for group in clusters]

    return clusters
