#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import dataclasses
import json
import logging
import math
import dataclass_wizard
import random
from typing import List, Optional, Set, Dict, Tuple
from pathlib import Path

from item import Item, ItemType, ItemQuality, PriceCategory, price_category_from_price
from npc import Npc, InventoryNode
from npc_template import NpcTemplate
from stats import StatType
from utils import left_align

RANDOM_GENERATING_NUM_ATTEMPTS: int = 100
MAX_AMMO_PER_MODIFICATION: int = 80


def choose_exponential_random_element(elements, reverse: bool = False):
    def generate_exponential_random(lambda_param):
        u = random.random()
        return -math.log(1 - u) / lambda_param

    exp_values = [generate_exponential_random(1.0) for _ in elements]
    total = sum(exp_values)
    probabilities = [v / total for v in exp_values]
    if reverse:
        probabilities = [1.0 - p for p in probabilities]

    return random.choices(elements, weights=probabilities, k=1)[0]


def load_data(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_cyberware(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating cyberware...")

    all_cyberware: List[Item] = list()
    for path in Path("Configs/items/cyberware").glob('**/*.json'):
        data = load_data(str(path))
        all_cyberware += [dataclass_wizard.fromdict(Item, x) for x in data]

    cyberware_budget: int = round(npc_template.rank.items_budget[ItemType.CYBERWARE].generate())
    logging.debug(f"\t{cyberware_budget=}")

    humanity_budget: int = npc.stats[StatType.EMP] * 10
    logging.debug(f"\t{humanity_budget=}")

    logging.debug(f"\t{npc_template.role.preferred_cyberware=}")

    npc.cyberware = InventoryNode(next(cw for cw in all_cyberware if cw.name == "Meatbody"))

    def pick_cyberware(cyberware_name: str,
                       starting_remaining_money_budget: int,
                       starting_remaining_humanity_budget: int,
                       current_cyberware_node_root: InventoryNode,
                       offset: int) -> Tuple[Optional[InventoryNode], int, int]:
        nonlocal all_cyberware

        cyberware_item: Item = next(cw for cw in all_cyberware if cw.name == cyberware_name)
        logging.debug(left_align(f"Trying to add: {cyberware_name}", offset))

        # try to check if this cyberware was already added
        already_added: bool = False

        def check_was_added(inventory_node: InventoryNode) -> bool:
            nonlocal cyberware_item
            nonlocal already_added

            already_added = inventory_node.item == cyberware_item
            return already_added

        current_cyberware_node_root.traverse_bfs(check_was_added)
        if already_added:
            logging.debug(left_align("Already added, skipping", offset + 1))
            return None, 0, 0

        container_where_added: Optional[Item] = None

        def try_add_to_inventory_node(inventory_node: InventoryNode) -> bool:
            nonlocal cyberware_item
            nonlocal container_where_added

            if inventory_node.add_child(cyberware_item):
                container_where_added = inventory_node.item
                return True
            else:
                return False

        def try_buy_cyberware(cyberware_to_buy: Item,
                              root: InventoryNode,
                              purchase_money_budget: int,
                              purchase_humanity_budget: int) -> Tuple[Optional[InventoryNode], int, int]:
            nonlocal offset

            if cyberware_to_buy.price > purchase_money_budget:
                logging.debug(left_align(
                    f"Not enough money to buy this cyberware "
                    f"(required: {cyberware_to_buy.price}, available: {purchase_money_budget})",
                    offset + 1))

                return None, 0, 0

            if cyberware_to_buy.max_humanity_loss > purchase_humanity_budget:
                logging.debug(left_align(
                    f"Not enough humanity to add this cyberware "
                    f"(required: {cyberware_to_buy.max_humanity_loss}, available: {purchase_humanity_budget})",
                    offset + 1))

                return None, 0, 0

            root.traverse_bfs(try_add_to_inventory_node)
            if not container_where_added:
                logging.debug(left_align(f"Couldn't find a suitable container", offset + 1))
                return None, 0, 0

            logging.debug(left_align(f"Found a suitable container: {container_where_added}", offset + 1))
            logging.debug(left_align(f"Pre-added: {cyberware_to_buy}", offset + 1))
            return (root,
                    purchase_money_budget - cyberware_to_buy.price,
                    purchase_humanity_budget - cyberware_to_buy.max_humanity_loss)

        # try to add this cyberware to an existing container
        purchase_new_root, purchase_remaining_cyberware_budget, purchase_remaining_humanity_budget = (
            try_buy_cyberware(
                cyberware_item,
                current_cyberware_node_root,
                starting_remaining_money_budget,
                starting_remaining_humanity_budget))

        if purchase_new_root:
            return purchase_new_root, purchase_remaining_cyberware_budget, purchase_remaining_humanity_budget

        # try to add all the required containers and then add the cyberware
        logging.debug(left_align(f"Creating required containers: {cyberware_item.requires_container}", offset + 1))
        containers_new_root: Optional[InventoryNode] = None
        containers_remaining_money_budget: int = starting_remaining_money_budget
        containers_remaining_humanity_budget: int = starting_remaining_humanity_budget
        for container in cyberware_item.requires_container:
            this_container_new_root, this_container_remaining_money_budget, this_container_remaining_humanity_budget = (
                pick_cyberware(
                    container,
                    starting_remaining_money_budget,
                    starting_remaining_humanity_budget,
                    copy.deepcopy(current_cyberware_node_root),
                    offset + 1))

            if this_container_new_root:
                containers_new_root = this_container_new_root
                containers_remaining_money_budget = this_container_remaining_money_budget
                containers_remaining_humanity_budget = this_container_remaining_humanity_budget
                break

        if not containers_new_root:
            logging.debug(left_align(f"Couldn't create any of required containers", offset + 1))
            return None, 0, 0

        logging.debug(left_align(f"Created all the required containers", offset + 1))
        return try_buy_cyberware(cyberware_item,
                                 containers_new_root,
                                 containers_remaining_money_budget,
                                 containers_remaining_humanity_budget)

    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        chosen_cyberware: str = choose_exponential_random_element(npc_template.role.preferred_cyberware)
        new_cyberware_node_root, remaining_cyberware_budget, remaining_humanity_budget = pick_cyberware(
            chosen_cyberware,
            cyberware_budget,
            humanity_budget,
            copy.deepcopy(npc.cyberware),
            1)

        if new_cyberware_node_root:
            npc.cyberware = new_cyberware_node_root
            cyberware_budget = remaining_cyberware_budget
            humanity_budget = remaining_humanity_budget
            logging.debug(f"\t\tAdded: {chosen_cyberware} and all the required containers")
            logging.debug(f"\t\t{remaining_cyberware_budget=}")
            logging.debug(f"\t\t{remaining_humanity_budget=}")

    npc.stats[StatType.EMP] = math.floor(humanity_budget / 10)
    logging.debug(f"\tHumanity left: {humanity_budget}")
    logging.debug(f"\tResulting EMP: {npc.stats[StatType.EMP]}")

    return npc


def generate_armor(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating armor...")
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
    logging.debug(f"\tPicked: npc.armor_body={npc.armor_body}")

    head_armor_budget: int = total_armor_budget - npc.armor_body.price if npc.armor_body else total_armor_budget
    logging.debug(f"\t{head_armor_budget=}")
    npc.armor_head = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class)
    logging.debug(f"\tPicked: npc.armor_head={npc.armor_head}")

    return npc


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


def generate_equipment(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating equipment...")
    data = load_data("Configs/items/equipment.json")

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

        selected_equipment = choose_exponential_random_element(preferred_equipment, True)
        logging.debug(f"\tTrying to generate equipment item: {selected_equipment}")
        equipment_item: Item = next(e for e in equipment if e.name == selected_equipment)

        if equipment_item in npc.inventory:
            logging.debug(f"\t\tFailed, already has {equipment_item})")
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

    return npc


def generate_drugs(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating drugs...")
    if len(list(filter(lambda i: i.name == "Airhypo", npc.inventory.keys()))):
        logging.debug("\tFound Airhypo, continuing...")
        data = load_data("Configs/items/drugs.json")

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


def generate_junk(npc: Npc, npc_template: NpcTemplate) -> Npc:
    # junk sources:
    # https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Junk
    # https://www.reddit.com/r/cyberpunkred/comments/13cef95/if_your_murderhobos_are_anything_like_mine_they/
    logging.debug("\nGenerating junk...")
    data = load_data("Configs/items/junk.json")

    junk: List[Item] = [dataclass_wizard.fromdict(Item, x) for x in data]
    junk.sort(key=lambda x: x.price)

    junk_budget: int = round(npc_template.rank.items_budget[ItemType.JUNK].generate())
    logging.debug(f"\t{junk_budget=}")

    max_junk_items: int = max(round(npc_template.rank.items_num_budget[ItemType.JUNK].generate()), 0)
    logging.debug(f"\t{max_junk_items=}")

    num_junk_items: int = 0
    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        if num_junk_items == max_junk_items:
            logging.debug(f"\tMax number of junk items reached: {max_junk_items}")
            break

        selected_junk = choose_exponential_random_element(junk, True)
        logging.debug(f"\tTrying to generate junk item: {selected_junk}")

        if selected_junk in npc.inventory:
            logging.debug(f"\t\tFailed, already has {selected_junk})")
            continue

        if selected_junk.price > junk_budget:
            logging.debug(
                f"\t\tFailed, not enough money (required: {selected_junk.price}, available: {junk_budget})")
            continue

        junk_budget -= selected_junk.price
        npc.inventory[selected_junk] = 1
        logging.debug(f"\t\tSucceed, added {selected_junk}")
        logging.debug(f"\t\tMoney left: {junk_budget}")

        num_junk_items += 1

    return npc


def create_equipment(npc: Npc, npc_template: NpcTemplate) -> Npc:
    npc = generate_cyberware(npc, npc_template)
    npc = generate_armor(npc, npc_template)
    npc = generate_weapon(npc, npc_template)
    npc = generate_ammo(npc, npc_template)
    npc = generate_equipment(npc, npc_template)
    npc = generate_drugs(npc, npc_template)
    npc = generate_junk(npc, npc_template)
    return npc
