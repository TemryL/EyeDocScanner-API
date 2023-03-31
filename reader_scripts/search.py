import config
import regex
from models.candidate import Candidate


def fuzzy_search(pattern, string, error_max):
    """Find approximately matching pattern in string

    Args:
        pattern (string): regex pattern
        string (string): where search is performed
        error_max (int)

    Returns:
        errors (int | None): None if no match
        regex_match (Match)
    """
    regex_pattern = f"({pattern}){{e<={error_max}}}"
    match = regex.search(regex_pattern, string, regex.BESTMATCH)

    if match is None:
        return None, None

    # match.fuzzy_counts: (n_substitutions, n_insertions, n_deletes)
    errors = sum(match.fuzzy_counts)

    return errors, match


def search_string(detected_text_list, pattern, region=None, n_candidates=1):
    """Searches for a string in all provided detected texts

    Args
        detected_text_list ([DetectedText])
        pattern (string): regex pattern
        region (BoundingBox | None): check if candidate bounding box's center
            is inside region
        n_candidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): n_candidates first candidates matching the
            pattern
    """

    candidates = []

    for detected_text in detected_text_list:
        if region is not None:
            center = detected_text.bbox.get_barycenter()
            if not region.contains_point(center):
                continue

        error, regex_match = fuzzy_search(
            pattern, detected_text.text, config.ERROR_MAX
        )

        if error is None:
            continue

        candidates.append(Candidate(detected_text, error, regex_match, region))

    candidates.sort(key=lambda c: c.errors)
    return candidates[:n_candidates]


def search_string_relative(
    reference,
    detected_text_list,
    pattern,
    region,
    region_is_relative=True,
    n_candidates=1,
    include_reference=False,
):
    """Searches for a string relative to a reference

    Args:
        reference (Candidate)
        detected_text_list ([detected_text])
        pattern (string): regex pattern
        region (BoundingBox)
        region_is_relative (bool): if True, region is relative to reference's
            center and in units of reference.line_height
        n_candidates (int): number of candidates to return
        include_reference (bool): if True, include the cropped reference in the
            search

    Returns:
        candidates ([Candidates]): n_candidates first candidates. May return
            an element which is not originally in detected_text_list if
            include_reference is True.
    """
    # Compute absolute region
    if region_is_relative:
        region = region.copy()
        ref_center = reference.detected_text.bbox.get_barycenter()
        line_height = reference.detected_text.line_height
        for p in region.points:
            p.x *= line_height
            p.y *= line_height
            p.x += ref_center.x
            p.y += ref_center.y

    # If reference included:
    # Build modified detected_text_list not containing the full "reference"
    # text, which may contain a match before reference's end index.
    # Example: reference text is "unwanted-value key: value", we should
    # prevent "unwanted-value" from matching.
    if include_reference:
        detected_text_list = (
            detected_text_list.copy()
        )  # don't mutate original list
        if reference.detected_text in detected_text_list:
            detected_text_list.remove(reference.detected_text)
        cropped = reference.detected_text.copy()
        cropped.text = cropped.text[reference.regex_match.span()[1] :]
        detected_text_list.append(cropped)

    return search_string(detected_text_list, pattern, region, n_candidates)


def search_string_on_right(
    reference, detected_text_list, pattern, region_width=None, n_candidates=1
):
    """Searches for a string on the right of a reference

    The checked region includes the reference bounding box, in case the
    searched string is inside the reference.

    Args:
        reference (Candidate)
        detected_text_list ([detected_text])
        pattern (string): regex pattern
        region_width (float): width added to the reference bounding box where
            text is searched.
            added width = reference.line_height * region_width.
            If None, search the whole srceen width.
        n_candidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): n_candidates first candidates. May return
            an element which is not originally in detected_text_list.
    """

    # Create searched region by expanding the reference's bounding box
    region = reference.detected_text.bbox.copy()
    if region_width is not None:
        added_width = region_width * reference.detected_text.line_height
    else:
        added_width = 1  # full screen width
    region.bottom_right.x += added_width
    region.top_right.x += added_width

    return search_string_relative(
        reference,
        detected_text_list,
        pattern,
        region,
        region_is_relative=False,
        n_candidates=n_candidates,
        include_reference=True,
    )


def search_string_below(
    reference, detected_text_list, pattern, region_height=1, n_candidates=1
):
    """Searches for a string below a reference

    The checked region is the reference bounding box shifted down by one
    line_height.

    Args:
        reference (Candidate)
        detected_text_list ([detected_text])
        pattern (string): regex pattern
        region_height (float): height of the region where text is searched,
            in units of reference.line_height. A greater value extends the
            region downwards.
        n_candidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): n_candidates first candidates
    """

    # Create searched region by shifting the reference's bounding box down
    region = reference.detected_text.bbox.copy()
    line_height = reference.detected_text.line_height
    for p in region.points:
        p.y -= reference.detected_text.line_height
    # Change region height by expanding the bottom
    region.bottom_left.y -= (region_height - 1) * line_height
    region.bottom_right.y -= (region_height - 1) * line_height

    return search_string_relative(
        reference,
        detected_text_list,
        pattern,
        region,
        region_is_relative=False,
        n_candidates=n_candidates,
    )
