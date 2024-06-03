#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from dataclasses import dataclass


@dataclass
class NormalDistribution:
    mean: float = 0
    standard_deviation: float = 0

    def generate(self) -> float:
        return random.gauss(mu=self.mean, sigma=self.standard_deviation)
