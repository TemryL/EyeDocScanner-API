from reader_scripts.find_best_reader import find_best_reader
from reader_scripts.list_of_readers import readers
from utils.get_detected_text_from_json import get_detected_text_from_json


def process_data(in_data, desired_reader=None):
    print("Processing Incoming Data...")

    # Import detected text from OCR output
    detected_text_list = get_detected_text_from_json(in_data)
    
    # Define used reader
    if desired_reader is not None:
        reader = desired_reader
    else:
        # Find best reader for this data
        reader = find_best_reader(detected_text_list)
        if reader is None:
            print("Could not find a matching reader.")
            return None, False

    # Generate structured output
    out_data, filtered_detected_text, regions = reader.read(detected_text_list)
    
    return out_data, True