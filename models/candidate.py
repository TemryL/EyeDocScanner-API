class Candidate:
    """Container for DetectedText instance and fuzzy_search result"""

    def __init__(
        self, detected_text, errors, regex_match, region_searched=None
    ):
        self.detected_text = detected_text
        self.errors = errors
        self.regex_match = regex_match
        self.region_searched = region_searched
