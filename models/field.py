from models.bounding_box import BoundingBox


class Field:
    """Field searched by Readers

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match
        region (BoundingBox|None): region in which to look for pattern. If
            None, field is searched in the whole image.
        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        data_order ([int]|None): order in which keys should be reordered
        n_candidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        region=None,
        keys=[],
        data_order=None,
        n_candidates=None,
    ):
        self.name = name
        self.pattern = pattern
        self.region = region
        self.keys = keys
        self.keys_capture_ids = data_order
        self.n_candidates = n_candidates or 1


class FieldRelative(Field):
    """Field positioned relatively to another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        relative_to (str): name of relatively positioned field
        region_relative (BoundingBox): specified relative to reference's center
        and in units of reference's line_height

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        data_order ([int]|None): order in which keys should be reordered
        n_candidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        relative_to,
        region_relative,
        keys=[],
        data_order=None,
        n_candidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            data_order=data_order,
            n_candidates=n_candidates,
        )
        self.relative_to = relative_to
        self.region_relative = region_relative


class FieldOnRight(Field):
    """Field positioned on the right of another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        on_right_of (str): name of the reference field
        region_width (float|None): width added to the reference bounding box
            where text is searched.
            Added width = reference.line_height * region_width.
            If None, search the whole srceen width.

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        data_order ([int]|None): order in which keys should be reordered
        n_candidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        on_right_of,
        region_width=None,
        keys=[],
        data_order=None,
        n_candidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            data_order=data_order,
            n_candidates=n_candidates,
        )
        self.on_right_of = on_right_of
        self.region_width = region_width


class FieldBelow(Field):
    """Field positioned below another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        below (str): name of the reference field
        region_height (float): height of the region where text is searched,
            in units of reference.line_height. A greater value extends the
            region downwards.

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        data_order ([int]|None): order in which keys should be reordered
        n_candidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        below,
        region_height=1.0,
        keys=[],
        data_order=None,
        n_candidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            data_order=data_order,
            n_candidates=n_candidates,
        )
        self.below = below
        self.region_height = region_height


def field_from_conf(conf):
    conf = conf.copy()

    if "relative_to" in conf:
        conf["region_relative"] = BoundingBox.from_bounds(
            *conf["region_relative"]
        )
        return FieldRelative(**conf)

    elif "on_right_of" in conf:
        return FieldOnRight(**conf)

    elif "below" in conf:
        return FieldBelow(**conf)

    else:
        if "region" in conf:
            conf["region"] = BoundingBox.from_bounds(*conf["region"])
        return Field(**conf)
