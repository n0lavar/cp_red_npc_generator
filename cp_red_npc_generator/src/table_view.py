#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TableView:
    num_columns: int = field(default=3)
    indent: int = field(default=4)
    elements: List[List[str]] = field(default_factory=list)
    columns: List = field(default_factory=list)

    def __post_init__(self):
        assert self.num_columns >= 1
        self.columns = [[] for _ in range(self.num_columns)]

    def add(self, part: List[str], column_number: Optional[int] = None):
        if column_number is not None and column_number < len(self.columns):
            self.columns[column_number] += part
        else:
            self.elements.append(part)

    def __str__(self):
        sorted_parts = sorted(self.elements, key=lambda x: len(x), reverse=True)
        columns = self.columns

        for part in sorted_parts:
            min_length_index = min(range(len(columns)), key=lambda x: len(columns[x]))
            columns[min_length_index] += part

        columns = [column for column in columns if len(column)]
        result: str = ""
        if len(columns):
            max_vertical_length: int = max([len(column) for column in columns])
            max_horizontal_lengths: List[int] = [max([len(x) for x in column]) for column in columns]
            for i in range(max_vertical_length):
                for j in range(len(columns)):
                    if i < len(columns[j]):
                        result += f"{columns[j][i]:<{max_horizontal_lengths[j] + self.indent}}"
                    else:
                        result += " " * (max_horizontal_lengths[j] + self.indent)

                result += "\n"

        return result
