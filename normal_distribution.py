#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import random


@dataclass
class NormalDistribution:
    mean: float = 0
    standard_deviation: float = 0

    def generate(self):
        return random.gauss(mu=self.mean, sigma=self.standard_deviation)
