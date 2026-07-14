#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy as np


@dataclass
class NormalDistribution:
    mean: float = 0
    standard_deviation: float = 0

    def generate(self) -> float:
        return np.random.normal(self.mean, self.standard_deviation)
