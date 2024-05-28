#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import random
from typing import List, Dict

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from utils import load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element

MAX_AMMO_PER_MODIFICATION: int = 80


def generate_ammo(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating ammo...")
    data = load_data("Configs/items/ammo.json")

    required_ammo_types: Dict[str, int] = dict()

    def add_required_ammo_type(required_ammo_type: str, magazine_size: int):
        nonlocal required_ammo_types
        if required_ammo_type not in required_ammo_types or magazine_size > required_ammo_types[required_ammo_type]:
            required_ammo_types[required_ammo_type] = magazine_size

    add_required_ammo_type("Grenades", 1)
    if npc.primary_weapon:
        for ammo_type in npc.primary_weapon.ammo_types:
            add_required_ammo_type(ammo_type, npc.primary_weapon.magazine)
    if npc.secondary_weapon:
        for ammo_type in npc.secondary_weapon.ammo_types:
            add_required_ammo_type(ammo_type, npc.secondary_weapon.magazine)

    logging.debug(f"\t{required_ammo_types=}")

    ammo_budget: int = round(npc_template.rank.items_budget[ItemType.AMMO].generate())
    logging.debug(f"\t{ammo_budget=}")

    preferred_ammo_modifications: List[str] = npc_template.role.preferred_ammo
    logging.debug(f"\t{preferred_ammo_modifications=}")

    def try_add_ammo(ammo_type: str, ammo_modification: str, amount: int) -> bool:
        nonlocal ammo_budget
        nonlocal data
        nonlocal npc

        logging.debug(f"\tTrying to add ammo: {ammo_type=}, {ammo_modification=}, {amount=}")

        if ammo_modification not in data:
            logging.debug(f"\t\tFailed, unknown modification: {ammo_modification}")
            return False

        ammo_type_data = data[ammo_modification]
        if ammo_type not in ammo_type_data["types"]:
            logging.debug(f"\t\tFailed, {ammo_modification} doesn't support {ammo_type}")
            return False

        price: int = ammo_type_data["price"]
        price_per_one: int = round(price if ammo_type == "Grenades" or ammo_type == "Rockets" else (price / 10))
        price_per_amount: int = price_per_one * amount
        if price_per_amount > ammo_budget:
            logging.debug(
                f"\t\tFailed, not enough money (required: {price_per_amount}, available: {ammo_budget})")
            return False

        ammo_item: Item = Item(f"{ammo_type} ({ammo_modification})", ItemType.AMMO, price_per_one)
        if ammo_item in npc.inventory:
            num_ammo_already_added: int = npc.inventory[ammo_item]
        else:
            num_ammo_already_added: int = 0

        new_num_ammo: int = num_ammo_already_added + amount
        if new_num_ammo > MAX_AMMO_PER_MODIFICATION:
            logging.debug(
                f"\t\tFailed, too much of this type of ammo ({new_num_ammo=}, {MAX_AMMO_PER_MODIFICATION=})")
            return False

        npc.inventory[ammo_item] = new_num_ammo
        ammo_budget -= price_per_amount
        logging.debug(f"\t\tSucceed, added {amount} of {ammo_item}")
        logging.debug(f"\t\tMoney left: {ammo_budget}")
        return True

    def add_basic_ammo(ammo_type: str) -> bool:
        if ammo_type in required_ammo_types.keys() and "Basic" in preferred_ammo_modifications:
            return try_add_ammo(ammo_type, "Basic", max(20, required_ammo_types[ammo_type] * 2))
        else:
            return False

    add_basic_ammo("Bullets") or add_basic_ammo("Slugs") or add_basic_ammo("Arrows")

    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        required_ammo_type, magazine_size = random.choice(list(required_ammo_types.items()))
        try_add_ammo(required_ammo_type,
                     choose_exponential_random_element(preferred_ammo_modifications, True),
                     magazine_size)

    return npc
