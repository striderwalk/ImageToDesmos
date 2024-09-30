import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def remove_t_points(image_array):
    # Find the T.
    # The Point two marks where the line will be split.
    shape = np.array([[0, 2, 0], [1, 1, 1], [0, 0, 0]])

    # Four possible rotations.
    for _ in range(4):
        remove_points = []

        offset_point = np.argwhere(shape == 2)[0]

        match_case = shape.copy()
        match_case[offset_point] = 1

        # Get a sliding window veiw of the image.
        subarrays = sliding_window_view(image_array, (3, 3))

        matches = np.all(subarrays == match_case, axis=(2, 3))

        for index in np.argwhere(matches):

            remove_points.append(
                (index[0] + offset_point[0], index[1] + offset_point[1])
            )

        for point in remove_points:
            image_array[point] = 3

        shape = np.rot90(shape)
    return image_array


def remove_crosses(image_array):

    remove_points = []

    subarrays = sliding_window_view(image_array, (3, 3))
    case = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    matches = np.all(subarrays == case, axis=(2, 3))

    for index in np.argwhere(matches):
        remove_points.append((index[0] + 1, index[1]))
        remove_points.append((index[0] + 1, index[1] + 2))

    for point in remove_points:
        image_array[point] = 3
    return image_array
