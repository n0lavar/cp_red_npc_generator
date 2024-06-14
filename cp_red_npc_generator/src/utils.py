#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
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
