#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import dataclass_wizard
from typing import List, Optional

from item import Item, ItemType
from npc import Npc, InventoryNode
from npc_template import NpcTemplate
from utils import load_data


def generate_armor(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating armor...")

    # check if we already have a cyberware that can act like an armor
    armor_cyberware: Optional[Item] = None
    for cyberware in npc.cyberware:
        if "Armor" in cyberware.item.tags:
            armor_cyberware = cyberware.item
            break

    if armor_cyberware:
        logging.debug(f"\tArmor cyberware found: {armor_cyberware})")
        npc.armor_body = armor_cyberware
        npc.armor_head = armor_cyberware
    else:
        data = load_data("Configs/items/armor.json")

        # assume npc would select the best armor to protect himself
        all_armor: List[Item] = sorted([dataclass_wizard.fromdict(Item, x) for x in data],
                                       key=lambda x: x.price,
                                       reverse=True)

        total_armor_budget: int = round(npc_template.rank.items_budget[ItemType.ARMOR].generate())
        logging.debug(f"\t{total_armor_budget=}")
        logging.debug(f"\t{npc_template.role.preferred_armor_class=}")

        def pick_armor(budget: int, preferred_armor_class: int) -> Optional[Item]:
            nonlocal all_armor
            for armor in all_armor:
                if armor.price > budget:
                    continue
                if armor.armor_class > preferred_armor_class:
                    continue
                return armor

            return None

        body_armor_budget: int = round(total_armor_budget * 0.8)
        logging.debug(f"\t{body_armor_budget=}")
        npc.armor_body = pick_armor(body_armor_budget, npc_template.role.preferred_armor_class)
        if not npc.armor_body:
            body_armor_budget: int = total_armor_budget
            logging.debug(f"\t{body_armor_budget=}")
            npc.armor_body = pick_armor(body_armor_budget, npc_template.role.preferred_armor_class)

        head_armor_budget: int = total_armor_budget - npc.armor_body.price if npc.armor_body else total_armor_budget
        logging.debug(f"\t{head_armor_budget=}")
        npc.armor_head = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class)

    logging.debug(f"\tPicked: npc.armor_head={npc.armor_head}")
    logging.debug(f"\tPicked: npc.armor_body={npc.armor_body}")

    return npc
