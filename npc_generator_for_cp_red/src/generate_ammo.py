#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element

MAX_AMMO_PER_MODIFICATION: int = 80


def generate_ammo(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating ammo...")
    data = load_data("configs/items/ammo.json")

    @dataclass
    class AmmoData:
        magazine_size: int = 0
        ammo_added: int = 0

    required_ammo_types: Dict[str, AmmoData] = dict()

    def add_required_ammo_type(required_ammo_type: str, magazine_size: int):
        nonlocal required_ammo_types
        if (required_ammo_type not in required_ammo_types
                or magazine_size > required_ammo_types[required_ammo_type].magazine_size):
            required_ammo_types[required_ammo_type] = AmmoData(magazine_size, 0)

    add_required_ammo_type("Grenades", 1)
    for weapon in npc.weapons:
        for ammo_type in weapon.ammo_types:
            add_required_ammo_type(ammo_type, weapon.magazine)

    logging.debug(f"\t{required_ammo_types=}")

    ammo_budget: int = round(npc_template.rank.items_budget[ItemType.AMMO].generate())
    logging.debug(f"\t{ammo_budget=}")

    preferred_ammo_modifications: List[str] = npc_template.role.preferred_ammo
    logging.debug(f"\t{preferred_ammo_modifications=}")

    def try_add_ammo(ammo_type: str, ammo_modification: str, amount: int, budget: int) -> int:
        nonlocal data
        nonlocal npc
        nonlocal npc_template

        logging.debug(f"\tTrying to add ammo: {ammo_type=}, {ammo_modification=}, {amount=}")

        if not npc_template.generation_rules.allow_grenades and ammo_type == "Grenades":
            logging.debug(f"\t\tFailed, allow_grenades=False")
            return 0

        if ammo_modification not in data:
            logging.debug(f"\t\tFailed, unknown modification: {ammo_modification}")
            return 0

        ammo_type_data = data[ammo_modification]
        if ammo_type not in ammo_type_data["types"]:
            logging.debug(f"\t\tFailed, {ammo_modification} doesn't support {ammo_type}")
            return 0

        price: int = ammo_type_data["price"]
        price_per_one: int = price * 10 if ammo_type == "Grenades" or ammo_type == "Rockets" else price
        price_per_amount: int = price_per_one * amount
        if price_per_amount > budget:
            logging.debug(
                f"\t\tFailed, not enough money (required: {price_per_amount}, available: {budget})")
            return 0

        ammo_item: Item = Item(f"{ammo_type} ({ammo_modification})", ItemType.AMMO, price_per_one)
        if ammo_item in npc.inventory:
            num_ammo_already_added: int = npc.inventory[ammo_item]
        else:
            num_ammo_already_added: int = 0

        new_num_ammo: int = num_ammo_already_added + amount
        if new_num_ammo > MAX_AMMO_PER_MODIFICATION:
            logging.debug(
                f"\t\tFailed, too much of this type of ammo ({new_num_ammo=}, {MAX_AMMO_PER_MODIFICATION=})")
            return 0

        npc.inventory[ammo_item] = new_num_ammo
        logging.debug(f"\t\tSucceed, added {amount} of {ammo_item}")
        logging.debug(f"\t\tMoney left: {budget - price_per_amount}")
        return price_per_amount

    logging.debug(f"Adding preferred ammo...")
    if not npc_template.generation_rules.allow_non_basic_ammo:
        logging.debug(f"allow_non_basic_ammo=False, skipped")
    else:
        for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
            required_ammo_type = list(required_ammo_types.keys())[np.random.choice(len(required_ammo_types))]
            money_spent: int = try_add_ammo(required_ammo_type,
                                            choose_exponential_random_element(preferred_ammo_modifications),
                                            required_ammo_types[required_ammo_type].magazine_size,
                                            ammo_budget)
            if money_spent != 0:
                ammo_budget -= money_spent
                required_ammo_types[required_ammo_type].ammo_added += required_ammo_types[
                    required_ammo_type].magazine_size

    logging.debug(f"Adding basic ammo...")
    for required_ammo_type_name, required_ammo_type_data in required_ammo_types.items():
        total_required_ammo: int = required_ammo_type_data.magazine_size
        match required_ammo_type_name:
            case "Bullets" | "Arrows" | "Slugs":
                total_required_ammo = max(20, required_ammo_type_data.magazine_size * 2)
            case "Rockets":
                total_required_ammo = 4
            case "Net":
                total_required_ammo = 2

        left_required_ammo: int = total_required_ammo - required_ammo_type_data.ammo_added
        if left_required_ammo > 0:
            modification_name = next(modification_name
                                     for modification_name, modification_data in data.items()
                                     if required_ammo_type_name in modification_data["types"])
            try_add_ammo(required_ammo_type_name,
                         modification_name,
                         left_required_ammo,
                         999999)

    return npc
