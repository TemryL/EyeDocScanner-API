from models.point import Point


class BoundingBox:
    """Bounding box with four points

    Args:
        bottom_left (Point)
        bottom_right (Point)
        top_left (Point)
        top_right (Point)
    """

    def __init__(self, bottom_left, bottom_right, top_left, top_right):
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.top_left = top_left
        self.top_right = top_right

    @property
    def points(self):
        """Return list of points ordered to draw the bounding box"""
        return [
            self.bottom_left,
            self.bottom_right,
            self.top_right,
            self.top_left,
        ]

    def get_barycenter(self):
        center = Point(0.0, 0.0)

        for p in self.points:
            center.x += p.x
            center.y += p.y

        center.x /= 4
        center.y /= 4

        return center

    def contains_point(self, point):
        """Check if point is inside the bounding box

        Note: Assumes that boxes are rectangular and not rotated, to simplify
        computation.
        """
        if point.x < self.bottom_left.x:
            return False
        if point.y < self.bottom_left.y:
            return False
        if point.x > self.top_right.x:
            return False
        if point.y > self.top_right.y:
            return False
        return True

    def convert_to_absolute_coordinates(self, crop_region):
        """Converts the bounding box to absolute coordinates

        Args:
            crop_region (CropRegion)
        """

        self.bottom_left.convert_to_absolute_coordinates(crop_region)
        self.bottom_right.convert_to_absolute_coordinates(crop_region)
        self.top_left.convert_to_absolute_coordinates(crop_region)
        self.top_right.convert_to_absolute_coordinates(crop_region)

    def copy(self):
        return BoundingBox(
            self.bottom_left.copy(),
            self.bottom_right.copy(),
            self.top_left.copy(),
            self.top_right.copy(),
        )

    @staticmethod
    def from_data(data):
        """Creates new instance from dictionnary"""
        return BoundingBox(
            Point.from_data(data["bottomLeft"]),
            Point.from_data(data["bottomRight"]),
            Point.from_data(data["topLeft"]),
            Point.from_data(data["topRight"]),
        )

    @staticmethod
    def from_bounds(xmin, xmax, ymin, ymax):
        """Creates new instance from coordinates"""
        return BoundingBox(
            Point(xmin, ymin),
            Point(xmax, ymin),
            Point(xmin, ymax),
            Point(xmax, ymax),
        )
