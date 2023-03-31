from .crop_region import CropRegion
from .detected_text import DetectedText


class CroppedOcrResults:
    """OCR results for a cropped piece of the whole image

    The bounding boxes of the detected text are relative to the crop region.
    """

    def __init__(self, crop_region):
        self.crop_region = crop_region
        self.detected_text_list = []

    def get_absolute_detected_text_list(self):
        """Returns a list of DetectedText in absolute coordinates"""

        detected_text_list = []
        for detected_text in self.detected_text_list:
            absolute_detected_text = detected_text.copy()
            absolute_detected_text.bbox.convert_to_absolute_coordinates(
                self.crop_region
            )
            detected_text_list.append(absolute_detected_text)

        return detected_text_list

    @staticmethod
    def from_data(data):
        cropped_ocr_results = CroppedOcrResults(
            CropRegion.from_data(data.cropRegion)
        )

        for d in data.detectedTextList:
            cropped_ocr_results.detected_text_list.append(
                DetectedText.from_data(d)
            )

        return cropped_ocr_results
