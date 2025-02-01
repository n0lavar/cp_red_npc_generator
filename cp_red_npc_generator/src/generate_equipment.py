#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import dataclass_wizard
from typing import List, Optional

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element


def generate_equipment(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating equipment...")
    if not npc_template.generation_rules.allow_equipment:
        logging.debug("allow_equipment=False, skipping...")
    else:
        data = load_data("configs/items/equipment.json")

        equipment: List[Item] = [dataclass_wizard.fromdict(Item, x) for x in data]

        preferred_equipment: List[str] = npc_template.role.preferred_equipment
        logging.debug(f"\t{preferred_equipment=}")

        equipment_budget: int = round(npc_template.rank.items_budget[ItemType.EQUIPMENT].generate())
        logging.debug(f"\t{equipment_budget=}")

        max_equipment_items: int = max(round(npc_template.rank.items_num_budget[ItemType.EQUIPMENT].generate()), 0)
        logging.debug(f"\t{max_equipment_items=}")

        num_equipment_items: int = 0
        for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
            if num_equipment_items == max_equipment_items:
                logging.debug(f"\tMax number of equipment items reached: {max_equipment_items}")
                break

            selected_equipment = choose_exponential_random_element(preferred_equipment)
            logging.debug(f"\tTrying to generate equipment item: {selected_equipment}")
            equipment_item: Item = next(e for e in equipment if e.name == selected_equipment)

            if not npc_template.generation_rules.allow_drugs and "Airhypo" in equipment_item.get_all_tags():
                logging.debug(f"\t\tallow_drugs=False, an item with \"Airhypo\" tag is useless, skipping")
                continue

            if equipment_item in npc.inventory:
                logging.debug(f"\t\tFailed, already has {equipment_item})")
                continue

            similar_cyberware: Optional[Item] = None
            for cyberware in npc.cyberware:
                if equipment_item.contains_any_unique_tag_from(cyberware.item):
                    similar_cyberware = cyberware.item
                    break

            if similar_cyberware:
                logging.debug(f"\t\tFailed, similar cyberware found: {similar_cyberware})")
                continue

            if equipment_item.price > equipment_budget:
                logging.debug(
                    f"\t\tFailed, not enough money (required: {equipment_item.price}, available: {equipment_budget})")
                continue

            equipment_budget -= equipment_item.price
            npc.inventory[equipment_item] = 1
            preferred_equipment.remove(selected_equipment)
            logging.debug(f"\t\tSucceed, added {equipment_item}")
            logging.debug(f"\t\tMoney left: {equipment_budget}")

            num_equipment_items += 1

    logging.debug("\nGenerating money...")
    if not npc_template.generation_rules.allow_money:
        logging.debug("allow_money=False, skipping...")
    else:
        pocket_money: int = max(round(npc_template.rank.pocket_money.generate()), 0)
        if pocket_money > 0:
            eb_item = Item("Eddies", ItemType.JUNK, 1)
            npc.inventory[eb_item] = pocket_money

    return npc
