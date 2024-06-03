#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import math

RANDOM_GENERATING_NUM_ATTEMPTS: int = 200


def left_align(obj, offset: int = 0, char: str = "\t") -> str:
    return char * offset + obj


def choose_exponential_random_element(elements, reverse: bool = False):
    def generate_exponential_random(lambda_param):
        u = random.random()
        return -math.log(1 - u) / lambda_param

    exp_values = [generate_exponential_random(1.0) for _ in elements]
    total = sum(exp_values)
    probabilities = [v / total for v in exp_values]
    if reverse:
        probabilities = [1.0 - p for p in probabilities]

    return random.choices(elements, weights=probabilities, k=1)[0]


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
