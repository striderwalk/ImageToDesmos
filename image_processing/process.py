from PIL import Image, ImageFilter
import numpy as np

from .edge_dection import find_edges


def clear_outer(image_array):
    image_array[0, :] = 0
    image_array[-1, :] = 0
    image_array[:, 0] = 0
    image_array[:, -1] = 0
    return image_array


def resize_image(image):

    width, height = image.size
    new_width = min(400, width)
    # new_width = 1000
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)

    return image


def edge_detection(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def get_image_array(file_name):
    # Load the image.
    image = Image.open(file_name)

    # image = image.quantize(4)
    # image.save("output/quantize.png")

    # Format the image as grayscale.
    image = image.convert("L")

    # Convert to standard size.
    image = resize_image(image)

    # Convert to np array.
    image_array = np.array(image)

    # Find the edges.
    image_array = find_edges(image_array)

    # Remove  outer edges.
    image_array = np.delete(image_array, 0, axis=0)
    image_array = np.delete(image_array, 1, axis=0)

    image_array = np.delete(image_array, -1, axis=0)
    image_array = np.delete(image_array, -2, axis=0)
    image_array = np.delete(image_array, 0, axis=1)
    image_array = np.delete(image_array, 1, axis=1)

    image_array = np.delete(image_array, -1, axis=1)
    image_array = np.delete(image_array, -2, axis=1)
    # Trim the black edges.
    image_array = trim_array(image_array)

    return image_array


def trim_array(image_array):

    while np.all(image_array[0, :] == 0):
        image_array = np.delete(image_array, 0, axis=0)
    while np.all(image_array[-1, :] == 0):
        image_array = np.delete(image_array, -1, axis=0)

    while np.all(image_array[:, 0] == 0):
        image_array = np.delete(image_array, 0, axis=1)
    while np.all(image_array[:, -1] == 0):
        image_array = np.delete(image_array, -1, axis=1)

    return image_array
