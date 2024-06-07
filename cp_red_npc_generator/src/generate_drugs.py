#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import dataclass_wizard
from typing import List

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element

MAX_UNIQUE_DRUG_ITEMS: int = 2


def generate_drugs(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating drugs...")
    if len(list(filter(lambda i: i.name == "Airhypo", npc.inventory.keys()))):
        logging.debug("\tFound Airhypo, continuing...")
        data = load_data("configs/items/drugs.json")

        drugs: List[Item] = [dataclass_wizard.fromdict(Item, x) for x in data]

        preferred_drugs: List[str] = npc_template.role.preferred_drugs
        logging.debug(f"\t{preferred_drugs=}")

        drugs_budget: int = round(npc_template.rank.items_budget[ItemType.DRUG].generate())
        logging.debug(f"\t{drugs_budget=}")

        max_drugs_items: int = max(round(npc_template.rank.items_num_budget[ItemType.DRUG].generate()), 0)
        logging.debug(f"\t{max_drugs_items=}")

        num_drugs_items: int = 0
        for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
            if num_drugs_items == max_drugs_items:
                logging.debug(f"\tMax number of drugs items reached: {max_drugs_items}")
                break

            selected_drug = choose_exponential_random_element(preferred_drugs, True)
            logging.debug(f"\tTrying to generate drug item: {selected_drug}")
            drug_item: Item = next(d for d in drugs if d.name == selected_drug)

            if drug_item in npc.inventory and npc.inventory[drug_item] >= MAX_UNIQUE_DRUG_ITEMS:
                logging.debug(f"\t\tFailed, too much drugs of type {drug_item}: {npc.inventory[drug_item]}")
                continue

            if drug_item.price > drugs_budget:
                logging.debug(
                    f"\t\tFailed, not enough money (required: {drug_item.price}, available: {drugs_budget})")
                continue

            drugs_budget -= drug_item.price
            npc.inventory.setdefault(drug_item, 0)
            npc.inventory[drug_item] += 1
            logging.debug(f"\t\tSucceed, added {drug_item}")
            logging.debug(f"\t\tMoney left: {drugs_budget}")

            num_drugs_items += 1
    else:
        logging.debug("\tThere is no Airhypo, skipping...")

    return npc
