#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import numpy as np

RANDOM_GENERATING_NUM_ATTEMPTS: int = 200


def left_align(obj, offset: int = 0, char: str = "\t") -> str:
    return char * offset + obj


def choose_exponential_random_element(elements, reverse: bool = False, scale=1.0):
    weights = np.random.exponential(scale, len(elements))
    probabilities = weights / weights.sum()
    index = np.random.choice(len(elements), p=list(reversed(probabilities)) if reverse else probabilities)
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
