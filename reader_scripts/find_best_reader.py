import config
from reader_scripts import search
from reader_scripts.list_of_readers import readers


def find_best_reader(detected_text_list):
    best_error = config.ERROR_MAX + 1
    best_reader = None
    
    for reader in list(readers.values()):
        candidates = search.search_string(
            detected_text_list, reader.distinctive_pattern
        )
        if len(candidates) == 0:
            continue
        if candidates[0].errors < best_error:
            best_error = candidates[0].errors
            best_reader = reader

    if best_reader is not None:
        print(f"Best matching reader: {best_reader.name}")

    return best_reader
