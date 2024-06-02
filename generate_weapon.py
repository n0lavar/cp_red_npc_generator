#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import dataclass_wizard
import random
from typing import List, Optional, Set, Tuple
from dataclasses import dataclass, field, replace

from item import Item, ItemType, ItemQuality, PriceCategory, price_category_from_price
from npc import Npc, InventoryNode
from npc_template import NpcTemplate
from stats import StatType
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS


@dataclass(frozen=True, eq=True)
class ItemWithNames(Item):
    possible_names: Set[str] = field(default_factory=set, compare=False)


def pick_weapon(budget: int,
                preferred_weapons: Set[str],
                min_items_quality: ItemQuality,
                all_weapons: List[ItemWithNames],
                installed_cyberware: InventoryNode) -> Tuple[Optional[Item], int]:
    if len(preferred_weapons) == 0:
        return None, 0

    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        preferred_weapon: str = random.choice(list(preferred_weapons))
        for cyberware in installed_cyberware:
            if preferred_weapon in cyberware.item.tags:
                logging.debug(f"\t\tFound a cyberware that acts like a preferred weapon: {cyberware.item}")
                return cyberware.item, 0

        preferred_qualities: List[ItemQuality]
        match min_items_quality:
            case ItemQuality.POOR:
                preferred_qualities = [ItemQuality.POOR, ItemQuality.STANDARD, ItemQuality.EXCELLENT]
            case ItemQuality.STANDARD:
                preferred_qualities = [ItemQuality.STANDARD, ItemQuality.EXCELLENT]
            case ItemQuality.EXCELLENT:
                preferred_qualities = [ItemQuality.EXCELLENT]
            case _:
                raise AssertionError

        preferred_quality: ItemQuality = random.choice(list(preferred_qualities))
        logging.debug(f"\t\tChosen quality: {preferred_quality}")

        preferred_weapon_item: ItemWithNames = next(w for w in all_weapons if preferred_weapon in w.tags)
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

        if price > budget:
            logging.debug(f"\t\tFailed, not enough money: required={price}, available={budget}")
            return None, 0

        weapon_copy = copy.deepcopy(preferred_weapon_item)
        weapon = replace(weapon_copy,
                         price=price,
                         quality=preferred_quality,
                         name=f"{random.choice(list(weapon_copy.possible_names))} ({weapon_copy.name})")

        logging.debug(f"\t\tPicked weapon: {weapon}")
        logging.debug(f"\t\tMoney left: {budget - price}")
        return weapon, price

    return None, 0


def get_brawling_weapon_item(npc: Npc) -> Item:
    stat_value, stat_modifier = npc.get_stat_or_skill_value(StatType.BODY.name)
    total_body = stat_value + stat_modifier

    if total_body <= 4:
        boxing_dmg = "1d6"
    elif total_body <= 6:
        boxing_dmg = "2d6"
    elif total_body <= 10:
        boxing_dmg = "3d6"
    else:
        boxing_dmg = "4d6"

    martial_arts_skill = next((s for s in npc.skills if s.name == "MartialArts"), None)
    if martial_arts_skill:
        return Item(name="Martial Arts", type=ItemType.WEAPON, damage=boxing_dmg, rate_of_fire=2)
    else:
        return Item(name="Boxing", type=ItemType.WEAPON, damage=boxing_dmg, rate_of_fire=1)


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating weapons...")
    data = load_data("Configs/items/weapon.json")

    all_weapons: List[ItemWithNames] = [dataclass_wizard.fromdict(ItemWithNames, x) for x in data]

    total_weapons_budget: int = round(npc_template.rank.items_budget[ItemType.WEAPON].generate())
    logging.debug(f"\t{total_weapons_budget=}")

    # try to buy a primary weapon with 0.8 of total budget
    primary_weapon_budget: int = round(total_weapons_budget * 0.8)
    primary_weapon, primary_weapon_money_spent = pick_weapon(primary_weapon_budget,
                                                             npc_template.role.preferred_primary_weapons,
                                                             npc_template.rank.min_items_quality,
                                                             all_weapons,
                                                             npc.cyberware)

    # if failed, try to buy a primary weapon with the whole budget
    if not primary_weapon:
        primary_weapon, primary_weapon_money_spent = pick_weapon(total_weapons_budget,
                                                                 npc_template.role.preferred_primary_weapons,
                                                                 npc_template.rank.min_items_quality,
                                                                 all_weapons,
                                                                 npc.cyberware)

    if primary_weapon:
        npc.weapons.add(primary_weapon)

    # try to buy a secondary weapon with any budget left
    secondary_weapon, _ = pick_weapon(total_weapons_budget - primary_weapon_money_spent,
                                      npc_template.role.preferred_secondary_weapons,
                                      npc_template.rank.min_items_quality,
                                      all_weapons,
                                      npc.cyberware)
    if secondary_weapon:
        npc.weapons.add(secondary_weapon)

    # add all the rest weapons from the cyberware
    for cyberware in npc.cyberware:
        if cyberware.item.damage:
            npc.weapons.add(cyberware.item)

    # add boxing or martial arts
    npc.weapons.add(get_brawling_weapon_item(npc))

    return npc
