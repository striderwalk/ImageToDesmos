import numba
import numpy as np
import cv2


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

    from sklearn.cluster import DBSCAN

    def cluster(data, epsilon):
        db = DBSCAN(eps=epsilon).fit(data)
        labels = db.labels_  # labels of the found clusters
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters
        clusters = [data[labels == i] for i in range(n_clusters)]  # list of clusters
        return clusters, n_clusters

    x = cluster(np.argwhere(image_array == 1), 4)

    return x[0]

    # Frame size

    print("Grouping!\n")
    # Image.fromarray(image_array * 255).show()

    groups = []
    x = 0
    while len(np.argwhere(image_array == 1)) > 0:

        cv2.imshow("image", image_array * 255)
        cv2.waitKey(1)

        last_size = len(np.argwhere(image_array == 1))

        print(str(len(np.argwhere(image_array == 1))).ljust(20), x, end="\r")
        x += 1
        one = np.argwhere(image_array == 1)[0]
        image_array, group = find_point_group(image_array, tuple(one))

        if last_size == len(np.argwhere(image_array == 1)):
            # for p in np.argwhere(image_array == 1):
            #     groups.append([p])
            print("GROUPING ERROR")
            break

        groups.append(np.array(group))

    cv2.destroyAllWindows()
    return groups
