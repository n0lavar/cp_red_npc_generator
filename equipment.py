#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import dataclasses
import logging
import math

import dataclass_wizard
import random

from data import *

RANDOM_GENERATING_NUM_ATTEMPTS: int = 100
MAX_AMMO_PER_MODIFICATION: int = 80


def generate_cyberware(npc: Npc, npc_template: NpcTemplate) -> Npc:
    return npc


def generate_armor(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating armor...")
    with open("Configs/items/armor.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        # assume npc would select the best armor to protect himself
        all_armor: List[Item] = sorted([dataclass_wizard.fromdict(Item, x) for x in data],
                                       key=lambda x: x.price,
                                       reverse=True)

        total_armor_budget: int = round(npc_template.rank.items_budget[ItemType("armor")].generate())
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
        logging.debug(f"\tPicked: npc.armor_body={npc.armor_body}")

        head_armor_budget: int = total_armor_budget - npc.armor_body.price if npc.armor_body else total_armor_budget
        logging.debug(f"\t{head_armor_budget=}")
        npc.armor_head = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class)
        logging.debug(f"\tPicked: npc.armor_head={npc.armor_head}")

    return npc


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating weapons...")
    with open("Configs/items/weapon.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        @dataclass(frozen=True, eq=True)
        class ItemWithNames(Item):
            possible_names: Set[str] = field(default_factory=set)

        all_weapons: List[ItemWithNames] = [dataclass_wizard.fromdict(ItemWithNames, x) for x in data]

        def pick_weapon(budget: int, preferred_weapons: Set[str]) -> Optional[Item]:
            nonlocal npc_template, all_weapons

            if len(preferred_weapons) == 0:
                return None

            for i in range(RANDOM_GENERATING_NUM_ATTEMPTS):
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

        total_weapons_budget: int = round(npc_template.rank.items_budget[ItemType("weapon")].generate())
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


def generate_ammo(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating ammo...")
    with open("Configs/items/ammo.json", "r", encoding="utf-8") as f:
        data = json.load(f)

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

            ammo_item: Item = Item(f"{ammo_type} ({ammo_modification})", ItemType.AMMO, price)
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

        # add basic ammo
        if "Bullets" in required_ammo_types.keys() and "Basic" in preferred_ammo_modifications:
            try_add_ammo("Bullets", "Basic", max(20, required_ammo_types["Bullets"] * 2))
        elif "Slugs" in required_ammo_types.keys() and "Basic" in preferred_ammo_modifications:
            try_add_ammo("Slugs", "Basic", max(20, required_ammo_types["Slugs"] * 2))
        elif "Arrows" in required_ammo_types.keys() and "Basic" in preferred_ammo_modifications:
            try_add_ammo("Arrows", "Basic", 20)

        def exp_dist_func(lambda_: float, x: float) -> float:
            return lambda_ * pow(math.e, -lambda_ * x)

        ammo_modifications_weights = [exp_dist_func(0.4, x) for x in range(len(preferred_ammo_modifications))]
        for i in range(RANDOM_GENERATING_NUM_ATTEMPTS):
            required_ammo_type, magazine_size = random.choice(list(required_ammo_types.items()))
            try_add_ammo(required_ammo_type,
                         random.choices(preferred_ammo_modifications, weights=ammo_modifications_weights)[0],
                         magazine_size)

    return npc


def generate_equipment(npc: Npc, npc_template: NpcTemplate) -> Npc:
    return npc


def generate_junk(npc: Npc, npc_template: NpcTemplate) -> Npc:
    return npc


def create_equipment(npc: Npc, npc_template: NpcTemplate) -> Npc:
    npc = generate_cyberware(npc, npc_template)
    npc = generate_armor(npc, npc_template)
    npc = generate_weapon(npc, npc_template)
    npc = generate_ammo(npc, npc_template)
    npc = generate_equipment(npc, npc_template)
    npc = generate_junk(npc, npc_template)
    return npc
