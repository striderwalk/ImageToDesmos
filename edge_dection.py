import cv2
import numpy as np
import scipy


def G(length=9, sigma=1.0):

    ax = np.linspace(-(length - 1) / 2.0, (length - 1) / 2.0, length)
    gauss = np.exp(-np.square(ax) / (2 * np.square(sigma)))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def nms(G, theta):
    """Non Max Suppression"""

    M, N = G.shape
    Z = np.zeros((M, N), dtype=np.int32)  # resultant image
    angle = theta * 180.0 / np.pi  # max -> 180, min -> -180
    angle[angle < 0] += 180  # max -> 180, min -> 0

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            q = 255
            r = 255

            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                r = G[i, j - 1]
                q = G[i, j + 1]

            elif 22.5 <= angle[i, j] < 67.5:
                r = G[i - 1, j + 1]
                q = G[i + 1, j - 1]

            elif 67.5 <= angle[i, j] < 112.5:
                r = G[i - 1, j]
                q = G[i + 1, j]

            elif 112.5 <= angle[i, j] < 157.5:
                r = G[i + 1, j + 1]
                q = G[i - 1, j - 1]

            if (G[i, j] >= q) and (G[i, j] >= r):
                Z[i, j] = G[i, j]
            else:
                Z[i, j] = 0
    return Z


def threshold(img, lowThresholdRatio=0.06, highThresholdRatio=0.08):
    """
    Double threshold
    """

    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int32)

    weak = 25
    strong = 255

    strong_i, strong_j = np.where(img >= highThreshold)
    # zeros_i, zeros_j = np.where(img < lowThreshold)

    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return res


def hysteresis(img, weak, strong=255):
    M, N = img.shape

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if img[i, j] == weak:
                if (
                    (img[i + 1, j - 1] == strong)
                    or (img[i + 1, j] == strong)
                    or (img[i + 1, j + 1] == strong)
                    or (img[i, j - 1] == strong)
                    or (img[i, j + 1] == strong)
                    or (img[i - 1, j - 1] == strong)
                    or (img[i - 1, j] == strong)
                    or (img[i - 1, j + 1] == strong)
                ):
                    img[i, j] = strong
                else:
                    img[i, j] = 0
    return img


def scale(x):
    """scale between 0 and 255"""
    return (x - x.min()) / (x.max() - x.min()) * 255


def find_edges(image_array):
    return (cv2.Canny(image_array, 100, 100) >= 10).astype(np.uint8)
    # https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html

    image_array = scipy.ndimage.gaussian_filter(image_array, 0.6, radius=2)

    # horizontal gradient
    kernal = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    sobel_h = scipy.signal.convolve(image_array, kernal)

    # vertical gradient
    kernal = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    sobel_v = scipy.signal.convolve(image_array, kernal)

    theta = np.arctan2(sobel_v, sobel_h)

    G = scale(np.hypot(sobel_h, sobel_v))

    img = nms(G, theta)
    img = threshold(img)
    img = hysteresis(img, 10)
    print(np.max(img))
    return (img >= 10).astype(np.uint8)
    k = 0.4
    s = 0.99
    guas_1 = scipy.signal.convolve(image_array, G(sigma=s))
    guas_2 = scipy.signal.convolve(image_array, G(sigma=s * k))

    image_array = guas_1 - guas_2

    image_array = (image_array >= 0.85).astype(np.uint8)

    # image_array = scipy.ndimage.binary_erosion(image_array).astype(np.uint8)

    return image_array
