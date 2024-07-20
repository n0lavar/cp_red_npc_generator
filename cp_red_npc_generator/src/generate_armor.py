#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from dataclasses import replace

import dataclass_wizard
from typing import List, Optional, Tuple, Dict

from item import Item, ItemType, Modifier
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data


def pick_armor(budget: int, preferred_armor_class: int, all_armor: List[Item]) -> Tuple[Optional[Item], int]:
    for armor in all_armor:
        if armor.price > budget:
            logging.debug(f"\tFailed to pick, not enough money (required: {armor.price}, available: {budget})")
            continue

        if armor.armor_class > preferred_armor_class:
            logging.debug(f"\tFailed to pick, the armor class is too high: {armor.armor_class}")
            continue

        return armor, armor.price

    return None, 0


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
        npc.armor.add(armor_cyberware.clone(name=f"Head: {armor_cyberware.name}", price=0))
        npc.armor.add(armor_cyberware.clone(name=f"Body: {armor_cyberware.name}", price=0))
    else:
        data = load_data("configs/items/armor.json")

        # assume npc would select the best armor to protect himself
        all_armor: List[Item] = sorted([dataclass_wizard.fromdict(Item, x) for x in data],
                                       key=lambda x: x.price,
                                       reverse=True)

        total_armor_budget: int = round(npc_template.rank.items_budget[ItemType.ARMOR].generate())
        logging.debug(f"\t{total_armor_budget=}")
        logging.debug(f"\t{npc_template.role.preferred_armor_class=}")

        # try to buy a body armor with 0.8 of the total budget
        body_armor_budget: int = round(total_armor_budget * 0.8)
        logging.debug(f"\tTrying to pick a body armor with a budget of {body_armor_budget}")
        body_armor, body_armor_money_spent = pick_armor(body_armor_budget,
                                                        npc_template.role.preferred_armor_class,
                                                        all_armor)

        # if failed, try to buy a body armor with the whole budget
        if not body_armor:
            logging.debug(f"\tTrying to pick a body armor with a budget of {total_armor_budget}")
            body_armor, body_armor_money_spent = pick_armor(total_armor_budget,
                                                            npc_template.role.preferred_armor_class,
                                                            all_armor)

        if body_armor:
            logging.debug(f"\tAdded body armor: {body_armor}")
            npc.armor.add(body_armor.clone(name=f"Body: {body_armor.name}"))
        else:
            logging.debug(f"\tFailed to add a body armor")

        # try to buy a head armor with any budget left
        head_armor_budget: int = total_armor_budget - body_armor_money_spent
        logging.debug(f"\tTrying to pick a head armor with a budget of {head_armor_budget}")
        head_armor, _ = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class, all_armor)

        if head_armor:
            logging.debug(f"\tAdded head armor: {head_armor}")
            npc.armor.add(head_armor.clone(name=f"Head: {head_armor.name}"))
        else:
            logging.debug(f"\tFailed to add a head armor")

    if len(npc.armor):
        # erase all the negative modifiers
        all_armor_negative_modifiers: Dict[str, int] = dict()
        for armor in npc.armor:
            for modifier in armor.modifiers:
                if modifier.simple < 0:
                    all_armor_negative_modifiers.setdefault(modifier.name, 0)
                    if modifier.simple < all_armor_negative_modifiers[modifier.name]:
                        all_armor_negative_modifiers[modifier.name] = modifier.simple

            npc.armor.discard(armor)
            npc.armor.add(replace(armor, modifiers=[x for x in armor.modifiers if x.simple > 0]))

        # apply all the negative modifiers only once
        armor_with_negative_modifiers: Item = next(iter(npc.armor))
        npc.armor.discard(armor_with_negative_modifiers)
        npc.armor.add(replace(armor_with_negative_modifiers,
                              modifiers=armor_with_negative_modifiers.modifiers
                                        + [Modifier(name, value) for name, value in
                                           all_armor_negative_modifiers.items()]))

    # if there is a shield (in cyberware or equipment), add it as well
    shields = [item for item in npc.get_all_items() if "Shield" in item.unique_tags]
    for shield in shields:
        logging.debug(f"\tAdded shield: {shield}")
        npc.armor.add(shield)

    return npc
