#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import dataclass_wizard
from typing import List

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element


def generate_junk(npc: Npc, npc_template: NpcTemplate) -> Npc:
    # junk sources:
    # https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Junk
    # https://www.reddit.com/r/cyberpunkred/comments/13cef95/if_your_murderhobos_are_anything_like_mine_they/
    logging.debug("\nGenerating junk...")
    data = load_data("configs/items/junk.json")

    junk: List[Item] = [dataclass_wizard.fromdict(Item, x) for x in data]
    junk.sort(key=lambda x: x.price)

    junk_budget: int = round(npc_template.rank.items_budget[ItemType.JUNK].generate())
    logging.debug(f"\t{junk_budget=}")

    max_junk_items: int = max(round(npc_template.rank.items_num_budget[ItemType.JUNK].generate()), 0)
    logging.debug(f"\t{max_junk_items=}")

    num_junk_items: int = 0
    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        if num_junk_items == max_junk_items:
            logging.debug(f"\tMax number of junk items reached: {max_junk_items}")
            break

        selected_junk = choose_exponential_random_element(junk, True)
        logging.debug(f"\tTrying to generate junk item: {selected_junk}")

        if selected_junk in npc.inventory:
            logging.debug(f"\t\tFailed, already has {selected_junk})")
            continue

        if selected_junk.price > junk_budget:
            logging.debug(
                f"\t\tFailed, not enough money (required: {selected_junk.price}, available: {junk_budget})")
            continue

        junk_budget -= selected_junk.price
        npc.inventory[selected_junk] = 1
        logging.debug(f"\t\tSucceed, added {selected_junk}")
        logging.debug(f"\t\tMoney left: {junk_budget}")

        num_junk_items += 1

    return npc
