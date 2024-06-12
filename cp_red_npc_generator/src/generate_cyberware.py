#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import dataclasses
import logging
import math
import dataclass_wizard
import uuid
from typing import List, Optional
from pathlib import Path
from dataclasses import dataclass, field, replace

from item import Item, ItemType
from npc import Npc, InventoryNode
from npc_template import NpcTemplate
from stats import StatType
from utils import left_align, load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element


def create_paired_item(item: Item) -> Item:
    paired_item = copy.deepcopy(item)
    return replace(paired_item,
                   must_be_paired=False,
                   max_equipped_items=0,
                   id=str(uuid.uuid4()))


def generate_cyberware(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating cyberware...")

    all_cyberware: List[Item] = list()
    for path in Path("configs/items/cyberware").glob('**/*.json'):
        data = load_data(str(path))
        all_cyberware += [dataclass_wizard.fromdict(Item, x) for x in data]

    cyberware_budget: int = round(npc_template.rank.items_budget[ItemType.CYBERWARE].generate())
    logging.debug(f"\t{cyberware_budget=}")

    humanity_budget: int = npc.stats[StatType.EMP] * 10
    logging.debug(f"\t{humanity_budget=}")

    logging.debug(f"\t{npc_template.role.preferred_cyberware=}")

    npc.cyberware = InventoryNode(next(cw for cw in all_cyberware if cw.name == "Meatbody"))

    @dataclass
    class PickingResult:
        new_root: InventoryNode = field(default_factory=InventoryNode)
        new_money_budget: int = field(default=0)
        new_humanity_budget: int = field(default=0)
        picked_item: Item = field(default_factory=Item)
        picked_item_container: InventoryNode = field(default_factory=InventoryNode)

    def pick_cyberware(cyberware_item: Item,
                       starting_remaining_money_budget: int,
                       starting_remaining_humanity_budget: int,
                       current_cyberware_node_root: InventoryNode,
                       offset: int,
                       first_pairing_container: Optional[Item] = None) -> Optional[PickingResult]:
        nonlocal all_cyberware

        logging.debug(left_align(f"Trying to add: {cyberware_item}", offset))

        # try to check if this cyberware was already added
        if cyberware_item.max_equipped_items != 0:
            num_already_added: int = 0
            for cyberware in current_cyberware_node_root:
                if cyberware.item == cyberware_item:
                    num_already_added += 1

            if num_already_added >= cyberware_item.max_equipped_items:
                logging.debug(
                    left_align(f"Max number of {num_already_added} items already reached, skipping", offset))
                return None

        def try_buy_cyberware(cyberware_to_buy: Item,
                              root: InventoryNode,
                              purchase_money_budget: int,
                              purchase_humanity_budget: int) -> Optional[PickingResult]:
            nonlocal offset

            for cyberware in root:
                if cyberware.item.contains_any_tag_from(cyberware_to_buy):
                    logging.debug(left_align(
                        f"{cyberware.item} already contains tag from this cyberware",
                        offset))
                    return None

            if cyberware_to_buy.price > purchase_money_budget:
                logging.debug(left_align(
                    f"Not enough money to buy this cyberware "
                    f"(required: {cyberware_to_buy.price}, available: {purchase_money_budget})",
                    offset))

                return None

            if cyberware_to_buy.max_humanity_loss > purchase_humanity_budget:
                logging.debug(left_align(
                    f"Not enough humanity to add this cyberware "
                    f"(required: {cyberware_to_buy.max_humanity_loss}, available: {purchase_humanity_budget})",
                    offset))

                return None

            container_where_added: Optional[InventoryNode] = None
            for cyberware in root:
                if first_pairing_container:
                    if first_pairing_container.id == cyberware.item.id:
                        continue

                new_node: Optional[InventoryNode] = cyberware.add_child(cyberware_item)
                if not new_node:
                    continue

                container_where_added = cyberware
                break

            if not container_where_added:
                logging.debug(left_align(f"Couldn't find a suitable container", offset))
                return None

            logging.debug(left_align(f"Found a suitable container: {container_where_added.item}", offset))

            result: PickingResult = PickingResult(root,
                                                  purchase_money_budget - cyberware_to_buy.price,
                                                  purchase_humanity_budget - cyberware_to_buy.max_humanity_loss,
                                                  cyberware_to_buy,
                                                  container_where_added)

            if cyberware_item.must_be_paired:
                logging.debug(left_align(f"{cyberware_item} required a paired item, generating...", offset))
                result = pick_cyberware(
                    create_paired_item(cyberware_item),
                    result.new_money_budget,
                    result.new_humanity_budget,
                    copy.deepcopy(result.new_root),
                    offset + 1,
                    result.picked_item_container.item)

                if not result:
                    logging.debug(left_align(f"Failed, couldn't create a paired container", offset))
                    return None

                logging.debug(left_align(f"Successfully created a paired item: {result.picked_item}", offset))

            for required_cyberware in cyberware_item.required_cyberware:
                logging.debug(
                    left_align(f"{cyberware_item} required a cyberware: {required_cyberware}, generating...", offset))

                required_cyberware_item: Item = next(cw for cw in all_cyberware if cw.name == required_cyberware)

                result = pick_cyberware(
                    dataclasses.replace(required_cyberware_item, id=str(uuid.uuid4())),
                    result.new_money_budget,
                    result.new_humanity_budget,
                    copy.deepcopy(result.new_root),
                    offset + 1)

                if not result:
                    logging.debug(left_align(f"Failed, couldn't create a required cyberware", offset))
                    return None

                logging.debug(left_align(f"Successfully created a required cyberware: {result.picked_item}", offset))

            logging.debug(left_align(f"Pre-added: {cyberware_to_buy}", offset))
            return result

        # try to add this cyberware to an existing container
        purchase_result: Optional[PickingResult] = try_buy_cyberware(
            cyberware_item,
            current_cyberware_node_root,
            starting_remaining_money_budget,
            starting_remaining_humanity_budget)

        if purchase_result:
            return purchase_result

        # try to add all the required containers and then add the cyberware
        logging.debug(left_align(f"Creating required containers: {cyberware_item.requires_container}", offset))
        picking_result: Optional[PickingResult] = None
        for container in cyberware_item.requires_container:
            container_item: Item = next(cw for cw in all_cyberware if cw.name == container)
            this_container_picking_result: Optional[PickingResult] = pick_cyberware(
                dataclasses.replace(container_item, id=str(uuid.uuid4())),
                starting_remaining_money_budget,
                starting_remaining_humanity_budget,
                copy.deepcopy(current_cyberware_node_root),
                offset + 1)

            if this_container_picking_result:
                picking_result = this_container_picking_result
                break

        if not picking_result:
            logging.debug(left_align(f"Couldn't create any of required containers", offset))
            return None

        logging.debug(left_align(f"Created all the required containers", offset))
        return try_buy_cyberware(cyberware_item,
                                 picking_result.new_root,
                                 picking_result.new_money_budget,
                                 picking_result.new_humanity_budget)

    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        chosen_cyberware: str = choose_exponential_random_element(npc_template.role.preferred_cyberware)
        chosen_cyberware_item: Item = next(cw for cw in all_cyberware if cw.name == chosen_cyberware)
        chosen_cyberware_picking_result: Optional[PickingResult] = pick_cyberware(
            chosen_cyberware_item,
            cyberware_budget,
            humanity_budget,
            copy.deepcopy(npc.cyberware),
            2)

        if chosen_cyberware_picking_result:
            npc.cyberware = chosen_cyberware_picking_result.new_root
            cyberware_budget = chosen_cyberware_picking_result.new_money_budget
            humanity_budget = chosen_cyberware_picking_result.new_humanity_budget
            logging.debug(f"\t\tAdded: {chosen_cyberware} and all the required containers")
            logging.debug(f"\t\t{cyberware_budget=}")
            logging.debug(f"\t\t{humanity_budget=}")

    npc.stats[StatType.EMP] = math.floor(humanity_budget / 10)
    logging.debug(f"\tHumanity left: {humanity_budget}")
    logging.debug(f"\tResulting EMP: {npc.stats[StatType.EMP]}")

    return npc
