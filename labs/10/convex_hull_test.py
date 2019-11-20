import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget

from tasks import convex_hull

"""
Here you can test your gift wrapping algorithm.
Space = generate a new set of points and calculate the convex hull.
"""


class ConvexHull(QWidget):
    def __init__(self, point_count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Gift wrapping")

        self._width = 800
        self._height = self._width
        self.setFixedWidth(self._width)
        self.setFixedHeight(self._height)

        self.point_count = point_count
        self.random = random.Random()
        self.points = self.generate_points()
        self.hull = self.get_hull(self.points)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.points = self.generate_points()
            self.hull = self.get_hull(self.points)
            print("Points: ", self.points)
            print("Hull: ", self.hull)
            self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.pen().setWidth(1)

        ellipse_width = 5
        offset = ellipse_width / 2.0
        for (x, y) in self.points:
            painter.drawEllipse(x, y, ellipse_width, ellipse_width)

        painter.save()
        painter.setPen(QColor("red"))
        for i in range(len(self.hull)):
            start = self.hull[i]
            end = self.hull[(i + 1) % len(self.hull)]
            assert start in self.points
            assert end in self.points

            start_x = start[0] + offset
            start_y = start[1] + offset
            end_x = end[0] + offset
            end_y = end[1] + offset

            painter.drawLine(start_x, start_y, end_x, end_y)
        painter.restore()

        painter.end()

    def get_hull(self, points):
        return convex_hull(list(points)) or []

    def generate_points(self):
        offset = 100
        width = self._width - offset
        height = self._height - offset

        points = set()
        while len(points) < self.point_count:
            x = self.random.randint(offset, height)
            y = self.random.randint(offset, width)
            point = (x, y)
            if point in points:
                continue
            points.add((x, y))
        return list(points)


if __name__ == "__main__":
    app = QApplication([])
    maze = ConvexHull(20)
    maze.show()
    app.exec_()
