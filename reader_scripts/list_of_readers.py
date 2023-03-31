"""Load Readers from .json configuration files and provide lists of Readers"""

import json

from models.reader import Reader
from reader_scripts import patterns
from utils.get_list_of_json_paths import get_list_of_json_paths


def load_readers():
    paths = get_list_of_json_paths("readers")
    readers = {}

    for path in paths:
        with open(path) as f:
            reader_conf = replace_patterns(json.load(f))
            reader = Reader(reader_conf)
            readers[reader.name] = reader

    return readers


def replace_patterns(conf):
    # Replace name and distinctivePattern
    for key, value in conf.items():
        if isinstance(value, str):
            conf[key] = conf[key].format(patterns=patterns)

    # Replace patterns in fields
    for field_conf in conf["fields"]:
        for key, value in field_conf.items():
            if isinstance(value, str):
                field_conf[key] = field_conf[key].format(patterns=patterns)

    return conf


readers = load_readers()
names = list(readers.keys())
