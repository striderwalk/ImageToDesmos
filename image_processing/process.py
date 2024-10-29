import cv2
import numpy as np
from PIL import Image


def resize_image(image, scale):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    return image


class ImageArray:
    def __init__(self, filename, quantize=None, plot=None, scale=1):
        self.plot = plot

        # Load the image.
        image = Image.open(filename)
        # This denoise the image somewhat which improve edge detection
        # Or not
        if quantize:
            image = image.quantize(quantize)
            image.save("output/quantize.png")

        # Format the image as grayscale.
        image = image.convert("RGBA")
        image = image.convert("L")
        # Convert to standard size.
        image = resize_image(image, scale)

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
        if not self.plot:
            return

        Image.fromarray(self.array * 255).convert("RGBA").save(filename)

    def trim_array(self):
        # Remove  outer edges.
        while np.all(self.array[0, :] == 0):
            self.array = np.delete(self.array, 0, axis=0)
        while np.all(self.array[-1, :] == 0):
            self.array = np.delete(self.array, -1, axis=0)

        while np.all(self.array[:, 0] == 0):
            self.array = np.delete(self.array, 0, axis=1)
        while np.all(self.array[:, -1] == 0):
            self.array = np.delete(self.array, -1, axis=1)
