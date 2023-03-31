from models.bounding_box import BoundingBox


class DetectedText:
    """Container for text and bounding box

    Assumes that the bounding box's system of coordinates has its origin at
    the bottom left corner of the image/screen.

    Args:
        text (string)
        bbox (BoundingBox)
    """

    def __init__(self, text, bbox):
        self.text = text
        self.bbox = bbox

    @property
    def points(self):
        """Return list of points ordered to draw a bounding box"""
        return self.bbox.points

    @property
    def line_height(self):
        """Returns the bounding box height in 0 to 1 range"""
        return self.bbox.top_left.y - self.bbox.bottom_left.y

    @property
    def text_width(self):
        """Returns the bounding box width in 0 to 1 range"""
        return self.bbox.bottom_right.x - self.bbox.bottom_left.x

    def copy(self):
        return DetectedText(self.text, self.bbox.copy())

    @staticmethod
    def from_data(data):
        """Creates new instance from dictionnary"""
        return DetectedText(data.text, BoundingBox.from_data(data.bbox))
