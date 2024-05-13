#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from typing import List
import json
import random
import math
from datetime import datetime


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


def rand(distribution_dict) -> float:
    match distribution_dict["type"]:
        case "normal":
            return random.gauss(mu=distribution_dict["mean"],
                                sigma=distribution_dict["standard_deviation"])
        case _:
            print("Unsupported distribution")
            return 0


def generate_loot(rank_num: int):
    random.seed(datetime.now().timestamp())

    ranks: List[dict] = list()
    with open("Configs/ranks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for rank_dict in data:
            ranks.append(rank_dict)

    rank = ranks[rank_num]
    rank_name = rank["name"]
    money = max(math.floor(rand(rank["cost_distribution"])), 0)
    max_items: int = math.floor(max(
        rand(rank["items_number_distribution"]), 0))
    print(f"{rank_name} has items worth a total of {money}:")

    loot: List[dict] = list()
    with open("Configs/loot.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        for loot_dict in data:
            loot.append(loot_dict)

    money_left: int = money
    result = ""
    for i in range(max_items):
        item_generated = False
        while not item_generated:
            loot_index = math.floor(clamp(
                rand(rank["items_type_distribution"]), 0, len(loot) - 1))
            loot_index_cost = loot[loot_index]["cost"]

            if loot_index_cost > money_left:
                continue

            loot_index_items = loot[loot_index]["items"]
            item = loot_index_items[random.randint(
                0, len(loot_index_items) - 1)]

            if result.count(item):
                continue

            result += "* "
            result += item
            money_left -= loot_index_cost
            result += f" ({loot_index_cost})"
            result += "\n"
            item_generated = True

    if money_left > 0:
        result += f"* Деньги ({money_left})"

    print(result)
    return 0
