#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import math
import dataclass_wizard
from typing import List, Optional, Tuple, Dict
from pathlib import Path
from dataclasses import dataclass, field
from result import Result, is_err

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from inventory_node import InventoryNode
from stats import StatType
from utils import left_align, load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element, \
    LoggerLevelScope


def create_paired_item(item: Item) -> Item:
    return item.clone(must_be_paired=False, max_equipped_items=0)


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
    class CyberwareGenerationState:
        root: InventoryNode = field(default_factory=InventoryNode)
        money_budget: int = field(default=0)
        humanity_budget: int = field(default=0)

    def pick_cyberware(cyberware_item: Item,
                       starting_remaining_money_budget: int,
                       starting_remaining_humanity_budget: int,
                       current_cyberware_node_root: InventoryNode,
                       offset: int,
                       first_pairing_container: Optional[Item] = None) -> Optional[CyberwareGenerationState]:
        nonlocal all_cyberware

        logging.debug(left_align(f"Trying to add: {cyberware_item}", offset))

        # check if max number of this cyberware was already added
        if cyberware_item.max_equipped_items != 0:
            num_already_added: int = 0
            for cyberware in current_cyberware_node_root:
                if cyberware.item == cyberware_item:
                    num_already_added += 1

            if num_already_added >= cyberware_item.max_equipped_items:
                logging.debug(
                    left_align(f"Max number of {num_already_added} items already reached, skipping", offset))
                return None

        # check if can't hold more cyberware of this type
        for cyberware in current_cyberware_node_root:
            if cyberware.item.contains_any_tag_from(cyberware_item):
                logging.debug(left_align(
                    f"{cyberware.item} already contains tag from this cyberware",
                    offset))
                return None

        state: CyberwareGenerationState = CyberwareGenerationState(current_cyberware_node_root,
                                                                   starting_remaining_money_budget,
                                                                   starting_remaining_humanity_budget)

        # try to pick all dependent cyberware
        current_cyberware_numbers: Dict[str, int] = {}
        for cyberware in current_cyberware_node_root:
            current_cyberware_numbers.setdefault(cyberware.item.name, 0)
            current_cyberware_numbers[cyberware.item.name] += 1

        required_cyberware_numbers: Dict[str, int] = {}
        for required_cyberware in cyberware_item.required_cyberware:
            required_cyberware_numbers.setdefault(required_cyberware, 0)
            required_cyberware_numbers[required_cyberware] += 1

        for required_cyberware_name, required_cyberware_numbers_num in required_cyberware_numbers.items():
            if required_cyberware_name in current_cyberware_numbers.keys():
                required_cyberware_numbers_num -= current_cyberware_numbers[required_cyberware_name]

            for _ in range(required_cyberware_numbers_num):
                logging.debug(
                    left_align(f"{cyberware_item} required a cyberware: {required_cyberware_name}, generating...",
                               offset))

                required_cyberware_item: Item = next(
                    cw for cw in all_cyberware if cw.name == required_cyberware_name).clone()

                state = pick_cyberware(
                    required_cyberware_item,
                    state.money_budget,
                    state.humanity_budget,
                    copy.deepcopy(state.root),
                    offset + 1)

                if not state:
                    logging.debug(left_align(f"Failed, couldn't create a required cyberware", offset))
                    return None

                logging.debug(
                    left_align(f"Successfully created a required cyberware: {required_cyberware_item}", offset))

        def try_buy_cyberware(cyberware_to_buy: Item, state: CyberwareGenerationState) \
                -> Optional[Tuple[CyberwareGenerationState, Item]]:
            nonlocal offset

            if cyberware_to_buy.price > state.money_budget:
                logging.debug(left_align(
                    f"Not enough money to buy this cyberware "
                    f"(required: {cyberware_to_buy.price}, available: {state.money_budget})",
                    offset))

                return None

            if cyberware_to_buy.max_humanity_loss > state.humanity_budget:
                logging.debug(left_align(
                    f"Not enough humanity to add this cyberware "
                    f"(required: {cyberware_to_buy.max_humanity_loss}, available: {state.humanity_budget})",
                    offset))

                return None

            container_where_added: Optional[InventoryNode] = None
            for cyberware in state.root:
                if first_pairing_container and first_pairing_container.id == cyberware.item.id:
                    continue

                with LoggerLevelScope(logging.INFO):
                    new_node: Result[InventoryNode, str] = cyberware.add_child(cyberware_item, npc)
                if is_err(new_node):
                    logging.debug(left_align(f"{new_node.err_value}", offset))
                    continue

                container_where_added = cyberware
                break

            if not container_where_added:
                logging.debug(left_align(f"Couldn't find a suitable container", offset))
                return None

            logging.debug(left_align(f"Found a suitable container: {container_where_added.item}", offset))

            logging.debug(left_align(f"Pre-added: {cyberware_to_buy}", offset))
            return (CyberwareGenerationState(state.root,
                                             state.money_budget - cyberware_to_buy.price,
                                             state.humanity_budget - cyberware_to_buy.max_humanity_loss),
                    container_where_added.item)

        # try to add this cyberware to an existing container
        purchase_result: Optional[Tuple[CyberwareGenerationState, Item]] = try_buy_cyberware(cyberware_item,
                                                                                             state)

        if not purchase_result:
            # try to add all the required containers and then add the cyberware
            logging.debug(left_align(f"Creating required containers: {cyberware_item.requires_container}", offset))
            for container in cyberware_item.requires_container:
                container_item: Item = next(cw for cw in all_cyberware if cw.name == container).clone()
                picking_result: Optional[CyberwareGenerationState] = pick_cyberware(
                    container_item,
                    state.money_budget,
                    state.humanity_budget,
                    copy.deepcopy(state.root),
                    offset + 1)

                if picking_result:
                    purchase_result = picking_result, container_item
                    break

            if not purchase_result:
                logging.debug(left_align(f"Couldn't create some of required containers", offset))
                return None
            else:
                logging.debug(left_align(f"Created the all the required containers", offset))
                purchase_result = try_buy_cyberware(cyberware_item, purchase_result[0])

        if not purchase_result:
            logging.debug(left_align(f"Couldn't buy an item", offset))
            return None

        state = purchase_result[0]
        container_where_added = purchase_result[1]

        if cyberware_item.must_be_paired:
            logging.debug(left_align(f"{cyberware_item} required a paired item, generating...", offset))
            paired_item: Item = create_paired_item(cyberware_item)
            state = pick_cyberware(
                paired_item,
                state.money_budget,
                state.humanity_budget,
                copy.deepcopy(state.root),
                offset + 1,
                container_where_added)

            if not state:
                logging.debug(left_align(f"Failed, couldn't create a paired container", offset))
                return None
            else:
                logging.debug(left_align(f"Successfully created a paired item: {paired_item}", offset))

        return state

    for _ in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        chosen_cyberware: str = choose_exponential_random_element(npc_template.role.preferred_cyberware)
        chosen_cyberware_item: Item = next(cw for cw in all_cyberware if cw.name == chosen_cyberware)
        chosen_cyberware_picking_result: Optional[CyberwareGenerationState] = pick_cyberware(
            chosen_cyberware_item,
            cyberware_budget,
            humanity_budget,
            copy.deepcopy(npc.cyberware),
            2)

        if chosen_cyberware_picking_result:
            npc.cyberware = chosen_cyberware_picking_result.root
            cyberware_budget = chosen_cyberware_picking_result.money_budget
            humanity_budget = chosen_cyberware_picking_result.humanity_budget
            logging.debug(f"\t\tAdded: {chosen_cyberware} and all the required containers")
            logging.debug(f"\t\t{cyberware_budget=}")
            logging.debug(f"\t\t{humanity_budget=}")

    npc.stats[StatType.EMP] = math.floor(humanity_budget / 10)
    logging.debug(f"\tHumanity left: {humanity_budget}")
    logging.debug(f"\tResulting EMP: {npc.stats[StatType.EMP]}")

    return npc
