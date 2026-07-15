import json
import unittest
from itertools import product
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


class BaseTest(unittest.TestCase):
    @classmethod
    def argument_matrix(cls):
        ranks = cls._load_names("ranks.json")
        roles = cls._load_names("roles.json")
        return ({"rank": rank, "role": role} for rank, role in product(ranks, roles))

    @staticmethod
    def _load_names(config_name):
        with (PROJECT_DIR / "configs" / config_name).open(encoding="utf-8") as config_file:
            return [item["name"] for item in json.load(config_file)]