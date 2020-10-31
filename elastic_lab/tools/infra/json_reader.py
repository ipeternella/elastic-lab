"""
Reader and parser for json files.
"""
import json
import os
from typing import Dict
from typing import List
from typing import TypedDict

from elastic_lab.settings import ROOT_DIR


class SeedData(TypedDict):
    data: List[Dict]


def read_seed_json(relative_json_path: str) -> SeedData:
    """
    Loads seed jsons into memory.
    """
    json_path = os.path.join(ROOT_DIR, relative_json_path)

    with open(json_path) as json_file:
        json_data: SeedData = json.load(json_file)

        return json_data
