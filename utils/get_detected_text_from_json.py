from models.cropped_ocr_results import CroppedOcrResults


def get_detected_text_from_json(data):
    cropped_ocr_results_list = []
    for d in data:
        cropped_ocr_results_list.append(CroppedOcrResults.from_data(d))

    detected_text_list = []

    for cropped_ocr_results in cropped_ocr_results_list:
        detected_text_list.extend(
            cropped_ocr_results.get_absolute_detected_text_list()
        )

    detected_text_list = merge_all_superimposed(detected_text_list)

    return detected_text_list


def merge_all_superimposed(detected_text_list):
    filtered = []

    for detected_text in detected_text_list:
        must_add = True

        for kept_detected_text in filtered:
            # Check if bounding boxes are superimposed
            if detected_text.bbox.contains_point(
                kept_detected_text.bbox.get_barycenter()
            ) or kept_detected_text.bbox.contains_point(
                detected_text.bbox.get_barycenter()
            ):
                # Keep the longest text
                if len(detected_text.text) > len(kept_detected_text.text):
                    filtered.remove(kept_detected_text)
                    filtered.append(detected_text)
                must_add = False
                break

        if must_add:
            filtered.append(detected_text)

    return filtered
