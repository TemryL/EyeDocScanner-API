import config
from models.field import (
    FieldBelow,
    FieldOnRight,
    FieldRelative,
    field_from_conf,
)
from reader_scripts import search


class Reader:
    def __init__(self, conf):
        self.name = conf["name"]
        self.distinctive_pattern = conf["distinctive_pattern"]
        self.fields = []

        for field_conf in conf["fields"]:
            self.fields.append(field_from_conf(field_conf))

    def read(self, detected_text_list):
        """Build data from detected texts"""

        filtered_detected_text = set()
        field_candidates = {}
        data = []
        regions = []

        for field in self.fields:
            # Extract data and candidates
            new_data, best_ref, candidates = get_data_from_field(
                field, field_candidates, detected_text_list
            )

            # Populate filteredDetectedText
            for candidate in candidates:
                if candidate.detected_text not in detected_text_list:
                    continue
                filtered_detected_text.add(candidate.detected_text)

            if best_ref is not None:
                if best_ref.detected_text in detected_text_list:
                    filtered_detected_text.add(best_ref.detected_text)

            # Save region where field was shearched
            if len(candidates) > 0:
                region = candidates[0].region_searched
                if region is not None:
                    regions.append(region)

            # Save field candidates
            field_candidates[field.name] = candidates

            # If no keys provided, no need to save data
            if len(field.keys) == 0:
                continue

            # Reorder data if needed
            if field.keys_capture_ids is not None:
                new_data = [new_data[i] for i in field.keys_capture_ids]

            data.extend(new_data)

        return data, list(filtered_detected_text), regions


def get_data_from_field(field, field_candidates, detected_text_list):
    if isinstance(field, FieldOnRight):
        refs = field_candidates[field.on_right_of]
        new_data, best_ref, candidates, _ = search_data_relative(
            refs,
            field.keys,
            search.search_string_on_right,
            detected_text_list,
            field.pattern,
            field.region_width,
            field.n_candidates,
        )

    elif isinstance(field, FieldBelow):
        refs = field_candidates[field.below]
        new_data, best_ref, candidates, _ = search_data_relative(
            refs,
            field.keys,
            search.search_string_below,
            detected_text_list,
            field.pattern,
            field.region_height,
            field.n_candidates,
        )

    elif isinstance(field, FieldRelative):
        refs = field_candidates[field.relative_to]
        new_data, best_ref, candidates, _ = search_data_relative(
            refs,
            field.keys,
            search.search_string_relative,
            detected_text_list,
            field.pattern,
            field.region_relative,
            n_candidates=field.n_candidates,
            include_reference=True,
        )

    else:  # Non-relative field
        best_ref = None
        new_data, candidates, _ = search_data(
            field.keys,
            search.search_string,
            detected_text_list,
            field.pattern,
            field.region,
        )

    return new_data, best_ref, candidates


def search_data(keys, search_func, *args, **kwargs):
    """Searches a string and builds corresponding data

    Args:
        keys ([string]): keys of the data to build
        search_func (function): function to use to search the string
        *args: arguments passed to search_func
        **kwargs: keyword arguments passed to search_func

    Returns:
        new_data ([dict ot str:str]): data built from the search
        candidates ([Candidate]): candidates found by search_func
        errors (int): number of errors in the best match
    """

    new_data = []
    errors = config.ERROR_MAX

    candidates = search_func(*args, **kwargs)

    # Build list of values corresponding to each key
    if len(candidates) != 0:
        errors = candidates[0].errors

        matches = list(candidates[0].regex_match.groups())

        # Fuzzy search function always capture the whole pattern in 1st group
        if len(matches) > 1:  # Other groups captured, get rid of 1st (whole)
            matches = matches[1:]

    else:  # no match found, empty values
        matches = [""] * len(keys)

    # Populate newData
    for i in range(len(keys)):
        new_data.append({keys[i]: matches[i]})

    return new_data, candidates, errors


def search_data_relative(references, keys, search_func, *args, **kwargs):
    """Searches a string relative to a reference and builds corresponding data

    Args:
        references ([Candidate]): list of references to search relative to.
        keys ([string]): keys of the data to build
        search_func (function): function to use to search the string
        *args: arguments passed to search_func
        **kwargs: keyword arguments passed to search_func

    Returns:
        best_new_data ([dict ot str:str]): data built from the search
        best_reference (Candidate): reference that led to best match
        best_candidates ([Candidate]): candidates found by search_func
        best_errors (int): number of errors in the best match
    """

    new_data = [{key: ""} for key in keys]
    errors = config.ERROR_MAX

    if len(references) == 0:  # reference not found
        return new_data, None, [], errors

    # Test all references to find which one leads to best match
    best_new_data = new_data
    best_reference = None
    best_candidates = []
    best_errors = errors + 1

    for reference in references:
        new_data, candidates, errors = search_data(
            keys, search_func, reference, *args, **kwargs
        )
        if errors < best_errors:
            best_new_data = new_data
            best_reference = reference
            best_candidates = candidates
            best_errors = errors

    return best_new_data, best_reference, best_candidates, best_errors
