class CropRegion:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @staticmethod
    def from_data(data):
        return CropRegion(data.x, data.x, data.width, data.height)
