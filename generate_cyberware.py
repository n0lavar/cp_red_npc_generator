#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import math
import dataclass_wizard
from typing import List, Optional, Tuple
from pathlib import Path

from item import Item, ItemType
from npc import Npc, InventoryNode
from npc_template import NpcTemplate
from stats import StatType
from utils import left_align, load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element


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
