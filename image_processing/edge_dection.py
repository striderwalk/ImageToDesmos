import cv2
import numpy as np
import scipy
from PIL import Image


def G(length=9, sigma=1.0):

    ax = np.linspace(-(length - 1) / 2.0, (length - 1) / 2.0, length)
    gauss = np.exp(-np.square(ax) / (2 * np.square(sigma)))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def find_edges(array):
    array = cv2.Canny(array, 100, 200)
    return (array >= 10).astype(np.uint8)

    array = scipy.signal.convolve(array, G(sigma=0.7))

    # horizontal gradient
    kernal = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    sobel_h = scipy.signal.convolve(array, kernal)

    # vertical gradient
    kernal = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    sobel_v = scipy.signal.convolve(array, kernal)

    gradient = np.hypot(sobel_h, sobel_v)
    theta = np.arctan2(sobel_v, sobel_h)
    Image.fromarray(gradient).show()
    # Image.fromarray(theta * 255).show()
    exit()
    return (array >= 10).astype(np.uint8)

    k = 0.4
    s = 0.99
    guas_1 = scipy.signal.convolve(array, G(sigma=s))
    guas_2 = scipy.signal.convolve(array, G(sigma=s * k))

    array = guas_1 - guas_2

    array = (array >= 0.85).astype(np.uint8)

    # array = scipy.ndimage.binary_erosion(array).astype(np.uint8)

    return array
