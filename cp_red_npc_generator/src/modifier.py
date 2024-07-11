#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from dataclasses import dataclass, field
from typing import List


@dataclass
class Modifier:
    name: str

    # simply add or subtract
    simple: int = 0

    # lines of Python code that should set `new_modifier` value
    complicated: List[str] = field(default_factory=list)

    def apply(self, source: str, name: str, start_value: int, current_modifier: int) -> int:
        new_modifier: int = current_modifier
        if name.lower() == self.name.lower():
            if len(self.complicated):
                logging.debug(f"\t\tFound a complicated modifier: {source}")

                loc = {}
                exec("\n".join(self.complicated), locals(), loc)
                new_modifier = loc['new_modifier']
            else:
                logging.debug(f"\t\tFound a simple modifier: {source}")
                new_modifier = current_modifier + self.simple

            logging.debug(f"\t\t[{name}] modifier: {current_modifier} -> {new_modifier}, "
                          f"value: {start_value + current_modifier} -> {start_value + new_modifier}")

        return new_modifier


@dataclass
class ModifierSource:
    item_name: str
    value: int = 0
