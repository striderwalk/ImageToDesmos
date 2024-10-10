import matplotlib.patches as patches
from matplotlib import pyplot as plt


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_subrects(self):

        return [
            Rect(self.x, self.y, self.w / 2, self.h / 2),
            Rect(self.x + self.w / 2, self.y, self.w / 2, self.h / 2),
            Rect(self.x, self.y + self.h / 2, self.w / 2, self.h / 2),
            Rect(self.x + self.w / 2, self.y + self.h / 2, self.w / 2, self.h / 2),
        ]

    def __contains__(self, point):
        x = point[0]
        y = point[1]

        if self.x > x:
            return False
        if self.y > y:
            return False

        if self.x + self.w < x:
            return False

        if self.y + self.h < y:
            return False

        return True


class QuadTree:
    def __init__(self, boundary, capacity=10):

        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.subdivided = False

    def subdivide(self):

        if self.subdivided:
            return

        self.subdivided = True

        subrects = self.boundary.get_subrects()
        self.nw = QuadTree(subrects[0])
        self.ne = QuadTree(subrects[1])
        self.sw = QuadTree(subrects[2])
        self.se = QuadTree(subrects[3])

        for point in self.points:
            self.nw.insert(point)
            self.ne.insert(point)
            self.sw.insert(point)
            self.se.insert(point)

        # del self.points

    @property
    def children(self):
        if not self.subdivided:
            return []
        return [
            self.nw,
            self.ne,
            self.sw,
            self.se,
        ]

    def insert(self, point):
        point = list(point)

        if point not in self.boundary:
            return False

        if not self.subdivided:
            self.points.append(point)

            if len(self.points) > self.capacity:
                self.subdivide()
        else:

            self.nw.insert(point)
            self.ne.insert(point)
            self.sw.insert(point)
            self.se.insert(point)

    def get_subtree(self, point):
        point = list(point)

        if point not in self.boundary:
            return False

        if not self.subdivided:
            if point in self.points:
                return self
            else:
                return None

        for subtree in self.children:
            if point in subtree.boundary:
                return subtree.get_subtree(point)

        return None

    def graph(self, points):
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        children = find_children(self)
        print("Number of segments: %d" % len(children))
        areas = set()
        for child in children:
            areas.add(child.boundary.w * child.boundary.h)

        print("Minimum segment area: %.3f units" % min(areas))
        for child in children:
            plt.gcf().gca().add_patch(
                patches.Rectangle(
                    (child.boundary.x, child.boundary.y),
                    child.boundary.w,
                    child.boundary.h,
                    fill=False,
                )
            )

        x = [point[0] for point in points]
        y = [point[1] for point in points]
        plt.plot(x, y, "ro")  # plots the points as red dots
        plt.show()
        # return


def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += find_children(child)
    return children
