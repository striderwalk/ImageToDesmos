from math import sin, cos
import random
import timeit
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import numba


def find_edges(image):

    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def load(file_name):
    image = Image.open(file_name)

    return image


@numba.jit()
def find_edges_points(image_array):
    edge_point = []
    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            if image_array[i, j] == 1:
                edge_point.append((i, j))

    return edge_point


@numba.jit()
def find_lines(image_array, edge_points):

    high_pairs = set()
    print("edge%=", len(edge_points) / image_array.size)
    for theta in range(0, 360):
        cos_theta = cos(theta)
        sin_theta = sin(theta)
        for r in range(-1000, 1000):
            count = []
            for point in edge_points:
                y, x = point[0], point[1]
                if x * cos_theta + y * sin_theta - r < 1:
                    count.append(point)

                if len(count) > 200:
                    break

            if len(count) >= 100 and len(count) < 200:

                def f(x):
                    return x[0]

                def g(x):
                    return x[1]

                count.sort(key=f)
                count.sort(key=g)
                x1 = count[0][1]
                y1 = count[0][0]
                x2 = count[-1][1]
                y2 = count[-1][0]

                high_pairs.add((x1, y1, x2, y2))

    return high_pairs


@numba.jit()
def dis_to_nearest_edge(point, edge_points):
    min_distance = 1000000000
    for y, x in edge_points:
        dis = np.floor(np.sqrt((y - point[0]) ** 2 + (x - point[1]) ** 2))
        min_distance = min(min_distance, dis)

    return int(min_distance)


@numba.jit()
def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return (None, np.inf)

    # Center of circle
    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    return ((cx, cy), radius)


@numba.jit()
def find_circles(image_array, edge_points):

    for p1 in edge_points:
        for p2 in edge_points:
            for p3 in edge_points:
                ((cx, cy), radius) = define_circle(p1, p2, p3)
                count = 0

                for p4 in edge_points:
                    if (p4[0] - cx) ** 2 + (p4[1] - cy) ** 2 - radius < 1.0e-6:
                        count += 1
                print(count)
    # circles = set()

    return set((0, 0, 0))


def clear_outer(image_array):
    image_array[0, :] = 0
    image_array[-1, :] = 0
    image_array[:, 0] = 0
    image_array[:, -1] = 0
    return image_array


def resize_image(image):
    width, height = image.size
    new_width = min(200, width)
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    return image


def main():
    # "D:/Image_filters/lines/line5062014251101771877.jpg"
    # image = load("Pepsi-logo.png")
    image = load("circle.png")

    image = resize_image(image)
    image_grayscale = image.convert("L")

    edges = find_edges(image_grayscale)
    image_array = np.array(edges)
    image_array = clear_outer(image_array)

    image_array = np.minimum(image_array, np.ones(image_array.shape))
    print(f"{image_array=}")
    print("image size = ", len(image_array), len(image_array[0]))

    edge_points = find_edges_points(image_array)
    circles = find_circles(image_array, edge_points)
    # high_pairs = find_lines(image_array, edge_points)
    high_pairs = []

    print("DRAWING: ")
    print(f"{len(circles)} CIRLES")
    draw = ImageDraw.Draw(image)
    for circle in circles:
        x, y, r = circle
        r = random.randint(1, 128)
        g = random.randint(1, 128)
        b = random.randint(1, 128)

        draw.circle((x, y), r, fill=(255, 0, 0), width=1)
        print(f"(x-{x})^2 + (y-{y})^2 = {r*2}")

    for points in high_pairs:
        # theta, r = pair
        # # xcos(Θ) + ysin(Θ) = r

        # if sin(theta) == 0:
        #     theta += 1
        # if cos(theta) == 0:
        #     theta += 1
        # p1 = (0, r / sin(theta))
        # p2 = (r / cos(theta), 0)
        # # print((*p1, *p2))
        # draw.line((*p1, *p2), fill=(255, 255, 0), width=1)
        try:
            draw.line(points, fill=(255, 255, 0), width=1)
        except:
            print(f"{points=}")
    print(image.size)
    image.show()


if __name__ == "__main__":
    time = timeit.timeit(main, number=1)
    print(time)
