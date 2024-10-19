import cv2
import numpy as np
from PIL import Image


def resize_image(image):
    width, height = image.size
    new_width = min(400, width)
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    return image


class ImageArray:
    def __init__(self, filename):
        # Load the image.
        image = Image.open(filename)
        # Format the image as grayscale.
        image = image.convert("L")
        # Convert to standard size.
        image = resize_image(image)

        # This denoise the image somewhat which improve edge detection
        # Or not
        # image = image.quantize(4)
        # image.save("output/quantize.png")

        # Convert to np array.
        self.array = np.array(image)

        # Find the edges.
        self.find_edges()

        # Trim the black edges.
        self.trim_array()

    def find_edges(self):
        # Use Canny edge detection and filter
        self.array = (cv2.Canny(self.array, 100, 200) >= 10).astype(np.uint8)

    @property
    def size(self):
        return self.array.shape

    def get_points(self):
        return np.argwhere(self.array == 1)

    def save(self, filename):
        Image.fromarray(self.array * 255).convert("RGB").save(filename)

    def trim_array(self):
        # Remove  outer edges.

        # self.array = np.delete(self.array, 0, axis=0)
        # self.array = np.delete(self.array, 1, axis=0)

        # self.array = np.delete(self.array, -1, axis=0)
        # self.array = np.delete(self.array, -2, axis=0)
        # self.array = np.delete(self.array, 0, axis=1)
        # self.array = np.delete(self.array, 1, axis=1)

        # self.array = np.delete(self.array, -1, axis=1)
        # self.array = np.delete(self.array, -2, axis=1)
        while np.all(self.array[0, :] == 0):
            self.array = np.delete(self.array, 0, axis=0)
        while np.all(self.array[-1, :] == 0):
            self.array = np.delete(self.array, -1, axis=0)

        while np.all(self.array[:, 0] == 0):
            self.array = np.delete(self.array, 0, axis=1)
        while np.all(self.array[:, -1] == 0):
            self.array = np.delete(self.array, -1, axis=1)
