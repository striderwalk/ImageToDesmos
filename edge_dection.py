import numpy as np
import scipy


def G(length=9, sigma=1.0):

    ax = np.linspace(-(length - 1) / 2.0, (length - 1) / 2.0, length)
    gauss = np.exp(-np.square(ax) / (2 * np.square(sigma)))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def find_edges(image_array):

    # sobel_h = ndimage.sobel(image_array, 0)  # horizontal gradient

    # sobel_v = ndimage.sobel(image_array, 1)  # vertical gradient

    # image_array = np.sqrt(sobel_h**2 + sobel_v**2)

    # image_array *= 1 / np.max(image_array)
    # print(np.max(image_array))
    image_array = scipy.ndimage.gaussian_filter(image_array, 0.6)

    k = 0.4
    s = 0.95
    guas_1 = scipy.signal.convolve(image_array, G(sigma=s))
    guas_2 = scipy.signal.convolve(image_array, G(sigma=s * k))

    image_array = guas_1 - guas_2

    image_array = (image_array >= 0.85).astype(np.uint8)

    # image_array = scipy.ndimage.binary_erosion(image_array).astype(np.uint8)

    return image_array
