#!/usr/bin/python
# -*- coding: utf-8 -*-

import builtins
import json
import logging
import math
import sys
import types
import dataclasses
from typing import List
import numpy as np

RANDOM_GENERATING_NUM_ATTEMPTS: int = 200


def left_align(obj, offset: int = 0, char: str = "\t") -> str:
    return char * offset + obj


def choose_exponential_random_element(elements):
    def exponential_distribution_probability_density_function(x: float, lambda_: float) -> float:
        if x >= 0:
            return lambda_ * np.exp(-lambda_ * x)
        else:
            return 0

    weights: List[float] = [exponential_distribution_probability_density_function(x * 20 / len(elements), 0.2)
                            for x in range(len(elements))]
    probabilities: List[float] = [x / sum(weights) for x in weights]
    index: int = np.random.choice(len(elements), p=probabilities)
    return elements[index]


def load_data(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def clamp(n, min_value, max_value):
    if n < min_value:
        return min_value
    elif n > max_value:
        return max_value
    else:
        return n


class LoggerLevelScope:
    def __init__(self, temp_level: int):
        self.temp_level = temp_level

    def __enter__(self):
        logger = logging.getLogger()
        self.initial_level = logger.getEffectiveLevel()
        logger.setLevel(max(self.temp_level, self.initial_level))

    def __exit__(self, exception_type, exception_value, traceback):
        logger = logging.getLogger()
        logger.setLevel(self.initial_level)


def is_debugger_active() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


def get_allowed_items(items: List[str], normalized_index: float) -> List[str]:
    """

    :param items: all items list where the elements are sorted from the coolest one to the worst
    :param normalized_index: a number from 0 to 1 representing the index of the coolest allowed item
    :return: `items` but without the coolest items depending on normalized_index
    """
    sequence_len: int = len(items)
    index: int = math.floor((sequence_len - 1) * normalized_index)
    return items[index:sequence_len]


def args_to_str(args) -> str:
    result: str = ""
    for key, value in args.items():
        match type(value):
            case builtins.bool:
                result += f"--{key}" if value else f"--no-{key}"
            case types.NoneType:
                result += f"--no-{key}"
            case _:
                result += f"--{key}={value}"

        result += " "

    return result


def get_default_value(cls, field_name: str):
    for f in dataclasses.fields(cls):
        if f.name == field_name.replace("-", "_"):
            if f.default is not dataclasses.MISSING:
                return f.default
            if f.default_factory is not dataclasses.MISSING:  # Handle default_factory
                return f.default_factory()
    return None
