#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

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
        
    weights = [exponential_distribution_probability_density_function(x * 20 / len(elements), 0.2)
               for x in range(len(elements))]
    probabilities = [x / sum(weights) for x in weights]
    index = np.random.choice(len(elements), p=probabilities)
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
