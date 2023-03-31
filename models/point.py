class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def convert_to_absolute_coordinates(self, crop_region):
        self.x = self.x * crop_region.width + crop_region.x
        self.y = self.y * crop_region.height + crop_region.y

    def copy(self):
        return Point(self.x, self.y)

    @staticmethod
    def from_data(data):
        """Creates new instance from dictionnary"""
        return Point(data.x, data.y)
