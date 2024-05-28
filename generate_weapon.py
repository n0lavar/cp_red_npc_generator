#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import dataclasses
import logging
import dataclass_wizard
import random
from typing import List, Optional, Set

from item import Item, ItemType, ItemQuality, PriceCategory, price_category_from_price
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating weapons...")
    data = load_data("Configs/items/weapon.json")

    @dataclasses.dataclass(frozen=True, eq=True)
    class ItemWithNames(Item):
        possible_names: Set[str] = dataclasses.field(default_factory=set)

    all_weapons: List[ItemWithNames] = [dataclass_wizard.fromdict(ItemWithNames, x) for x in data]

    def pick_weapon(budget: int, preferred_weapons: Set[str]) -> Optional[Item]:
        nonlocal npc_template, all_weapons

        if len(preferred_weapons) == 0:
            return None

        for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
            preferred_qualities: List[ItemQuality]
            match npc_template.rank.min_items_quality:
                case ItemQuality.POOR:
                    preferred_qualities = [ItemQuality.POOR, ItemQuality.STANDARD, ItemQuality.EXCELLENT]
                case ItemQuality.STANDARD:
                    preferred_qualities = [ItemQuality.STANDARD, ItemQuality.EXCELLENT]
                case ItemQuality.EXCELLENT:
                    preferred_qualities = [ItemQuality.EXCELLENT]
                case _:
                    raise AssertionError

            preferred_weapon: str = random.choice(list(preferred_weapons))
            preferred_weapon_item: ItemWithNames = next(w for w in all_weapons if w.name == preferred_weapon)
            preferred_quality: ItemQuality = random.choice(list(preferred_qualities))
            initial_price_category: PriceCategory = price_category_from_price(preferred_weapon_item.price)
            price: int = preferred_weapon_item.price
            match preferred_quality:
                case ItemQuality.POOR:
                    if initial_price_category.value - 1 not in PriceCategory:
                        continue
                    price = PriceCategory(initial_price_category.value - 1).get_price()
                case ItemQuality.EXCELLENT:
                    if initial_price_category.value + 1 not in PriceCategory:
                        continue
                    price = PriceCategory(initial_price_category.value + 1).get_price()

            if price <= budget:
                weapon_copy = copy.deepcopy(preferred_weapon_item)
                weapon = dataclasses.replace(weapon_copy,
                                             price=price,
                                             quality=preferred_quality,
                                             name=f"{random.choice(list(weapon_copy.possible_names))} ({weapon_copy.name})")
                return weapon

        return None

    total_weapons_budget: int = round(npc_template.rank.items_budget[ItemType.WEAPON].generate())
    logging.debug(f"\t{total_weapons_budget=}")

    primary_weapon_budget: int = round(total_weapons_budget * 0.8)
    logging.debug(f"\t{primary_weapon_budget=}")
    npc.primary_weapon = pick_weapon(primary_weapon_budget, npc_template.role.preferred_primary_weapons)
    if not npc.primary_weapon:
        primary_weapon_budget: int = total_weapons_budget
        logging.debug(f"\t{primary_weapon_budget=}")
        npc.primary_weapon = pick_weapon(primary_weapon_budget, npc_template.role.preferred_primary_weapons)
    logging.debug(f"\tPicked: npc.primary_weapon={npc.primary_weapon}")

    secondary_weapon_budget: int = total_weapons_budget - npc.primary_weapon.price if npc.primary_weapon else total_weapons_budget
    logging.debug(f"\t{secondary_weapon_budget=}")
    npc.secondary_weapon = pick_weapon(secondary_weapon_budget, npc_template.role.preferred_secondary_weapons)
    logging.debug(f"\tPicked: npc.secondary_weapon={npc.secondary_weapon}")

    return npc
