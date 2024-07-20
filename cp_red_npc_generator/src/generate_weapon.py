#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import dataclass_wizard
import numpy as np
from typing import List, Optional, Set, Tuple, Dict
from dataclasses import dataclass, field, replace

from item import Item, ItemType, ItemQuality, PriceCategory
from npc import Npc
from npc_template import NpcTemplate
from stats import StatType, SkillType
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS


@dataclass(frozen=True, eq=True)
class ItemWithNames(Item):
    possible_names: Set[str] = field(default_factory=set, compare=False)


def pick_weapon(budget: int,
                preferred_weapons: Set[str],
                min_items_quality: ItemQuality,
                all_weapons: List[ItemWithNames],
                npc: Npc) -> Tuple[Optional[Item], int]:
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

    logging.debug(f"\tTrying to pick a weapon:")
    if len(preferred_weapons) == 0:
        logging.debug(f"\tNo preferred weapons, skipping...")
        return None, 0

    logging.debug(f"\t{budget=}")
    logging.debug(f"\t{preferred_weapons=}")
    logging.debug(f"\t{preferred_qualities=}")

    for num_attempt in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        logging.debug(f"\tGenerating, attempt {num_attempt}")
        preferred_weapon: str = np.random.choice(sorted(list(preferred_weapons)))
        for cyberware in npc.cyberware:
            if preferred_weapon in cyberware.item.unique_tags:
                logging.debug(f"\t\tFound a cyberware that acts like a preferred weapon: {cyberware.item}")
                return cyberware.item, 0

        preferred_weapon_item: ItemWithNames = next(w for w in all_weapons if preferred_weapon in w.unique_tags)
        for item in npc.get_all_items():
            if preferred_weapon_item.contains_any_unique_tag_from(item):
                logging.debug(f"\t\t{item} already acts like this weapon, skipping")
                return None, 0

        preferred_quality: ItemQuality = np.random.choice(preferred_qualities)
        logging.debug(f"\t\tChosen quality: {preferred_quality}")

        initial_price_category: PriceCategory = PriceCategory.from_price(preferred_weapon_item.price)
        price: int = preferred_weapon_item.price
        match preferred_quality:
            case ItemQuality.POOR:
                if initial_price_category.value - 1 in PriceCategory:
                    price = PriceCategory(initial_price_category.value - 1).get_default_price()
                else:
                    price = initial_price_category.value / 2
            case ItemQuality.EXCELLENT:
                if initial_price_category.value + 1 in PriceCategory:
                    price = PriceCategory(initial_price_category.value + 1).get_default_price()
                else:
                    price = initial_price_category.value * 2

        if price > budget:
            logging.debug(f"\t\tFailed, not enough money: required={price}, available={budget}")
            continue

        weapon_copy = copy.deepcopy(preferred_weapon_item)
        weapon = replace(
            weapon_copy,
            price=price,
            quality=preferred_quality,
            name=f"{np.random.choice(list(weapon_copy.possible_names))} ({weapon_copy.name})")

        logging.debug(f"\t\tPicked weapon: {weapon}")
        logging.debug(f"\t\tMoney left: {budget - price}")
        return weapon, price

    return None, 0


def get_brawling_weapon_item(npc: Npc) -> Item:
    total_body = npc.get_stat_or_skill_value(StatType.BODY.name).get_total()

    if total_body <= 4:
        boxing_dmg = "1d6"
    elif total_body <= 6:
        boxing_dmg = "2d6"
    elif total_body <= 10:
        boxing_dmg = "3d6"
    else:
        boxing_dmg = "4d6"

    martial_arts_skill = next(
        (skill for skill, level in npc.skills.items() if skill.name == "MartialArts" and level > 0), None)

    brawling_skill = Item(type=ItemType.WEAPON, damage=boxing_dmg, tags=["MeleeWeapon"], rate_of_fire=2)
    if martial_arts_skill:
        return replace(brawling_skill, name="Martial Arts", unique_tags=["MartialArts"])
    else:
        return replace(brawling_skill, name="Brawling", unique_tags=["Brawling"])


def add_weapon_to_npc(weapon: Item, npc: Npc, weapon_skills_data: Dict[str, str]):
    skill_name: Optional[str] = None
    for tag in weapon.get_all_tags():
        if tag in weapon_skills_data.keys():
            skill_name = weapon_skills_data[tag]
            break

    assert skill_name
    skill_value: int = npc.get_skill_total_value(skill_name)
    if weapon.quality == ItemQuality.EXCELLENT:
        skill_value += 1

    weapon = replace(
        weapon,
        name=f"[{skill_value}] {weapon.name}")

    npc.weapons.add(weapon)


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating weapons...")

    weapons_data = load_data("configs/items/weapon.json")
    all_weapons: List[ItemWithNames] = [dataclass_wizard.fromdict(ItemWithNames, x) for x in weapons_data]

    weapon_skills_data: Dict[str, str] = load_data("configs/weapon_skills.json")

    total_weapons_budget: int = round(npc_template.rank.items_budget[ItemType.WEAPON].generate())
    logging.debug(f"\t{total_weapons_budget=}")

    # try to buy a primary weapon with 0.8 of the total budget
    primary_weapon, primary_weapon_money_spent = pick_weapon(
        round(total_weapons_budget * 0.8),
        npc_template.role.preferred_primary_weapons,
        npc_template.rank.min_items_quality,
        all_weapons,
        npc)

    # if failed, try to buy a primary weapon with the whole budget
    if not primary_weapon:
        primary_weapon, primary_weapon_money_spent = pick_weapon(
            total_weapons_budget,
            npc_template.role.preferred_primary_weapons,
            npc_template.rank.min_items_quality,
            all_weapons,
            npc)

    if primary_weapon:
        add_weapon_to_npc(primary_weapon, npc, weapon_skills_data)

    # try to buy a secondary weapon with any budget left
    secondary_weapon, _ = pick_weapon(
        total_weapons_budget - primary_weapon_money_spent,
        npc_template.role.preferred_secondary_weapons,
        npc_template.rank.min_items_quality,
        all_weapons,
        npc)

    if secondary_weapon:
        add_weapon_to_npc(secondary_weapon, npc, weapon_skills_data)

    # add all the rest weapons from the cyberware
    for cyberware in npc.cyberware:
        if cyberware.item.damage:
            add_weapon_to_npc(cyberware.item, npc, weapon_skills_data)

    # add boxing or martial arts
    add_weapon_to_npc(get_brawling_weapon_item(npc), npc, weapon_skills_data)

    return npc
