#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import math
import dataclass_wizard
from typing import List, Optional, Dict
from pathlib import Path
from dataclasses import dataclass, field, replace
from result import Result, is_err

from item import Item, ItemType
from npc import Npc
from npc_template import NpcTemplate
from inventory_node import InventoryNode
from stats import StatType
from utils import left_align, load_data, RANDOM_GENERATING_NUM_ATTEMPTS, choose_exponential_random_element, \
    LoggerLevelScope, clamp, get_allowed_items


def create_paired_item(item: Item) -> Item:
    return item.clone(must_be_paired=False, max_equipped_items=0)


@dataclass
class CyberwareGenerationState:
    last_added_cyberware: Optional[InventoryNode] = field(default_factory=InventoryNode)
    root: InventoryNode = field(default_factory=InventoryNode)
    money_budget: int = field(default=0)
    humanity_budget: int = field(default=0)


def add_to_container(
        item: Item,
        container: InventoryNode,
        container_selection_normalized_index: float,
        npc: Npc,
        depth: int,
        first_pairing_container: Optional[InventoryNode]) -> Optional[InventoryNode]:
    if first_pairing_container and first_pairing_container.item.id == container.item.id:
        return None

    with LoggerLevelScope(logging.INFO):
        new_node: Result[InventoryNode, str] = container.add_child(item, npc, container_selection_normalized_index)

    if is_err(new_node):
        logging.debug(left_align(f"{new_node.err_value}", depth))
        return None

    return new_node.value


# check if we can add the item,
# add all the required dependant cyberware, containers,
# try to decrease the money and the humanity,
# and finally add the item to the cyberware tree
def add_cyberware(
        item: Item,
        state: CyberwareGenerationState,
        npc_template: NpcTemplate,
        all_cyberware: List[Item],
        npc: Npc,
        depth: int,
        # if specified, exclude this container from the set, where you can add this item
        first_pairing_container: Optional[InventoryNode] = None) \
        -> Optional[CyberwareGenerationState]:
    logging.debug(left_align(f"Trying to add: {item.name}", depth))

    if item.max_humanity_loss >= 4 and not npc_template.use_borgware:
        logging.debug(left_align(f"The item is a borgware and use_borgware is false", depth))
        return None

    # check if the max number of this cyberware was already added
    if item.max_equipped_items != 0:
        num_already_added: int = 0
        for cyberware in state.root:
            if cyberware.item == item:
                num_already_added += 1

        if num_already_added >= item.max_equipped_items:
            logging.debug(left_align(f"Max number of {num_already_added} items already reached, skipping", depth))
            return None

    # check if we can't hold more cyberware of this type
    for cyberware in state.root:
        # checking the name as it may be a paired item
        if cyberware.item.name != item.name and cyberware.item.contains_any_unique_tag_from(item):
            logging.debug(left_align(f"{cyberware.item} already contains tag from this cyberware", depth))
            return None

    # try to pick all dependent cyberware
    current_cyberware_numbers: Dict[str, int] = {}
    for cyberware in state.root:
        current_cyberware_numbers.setdefault(cyberware.item.name, 0)
        current_cyberware_numbers[cyberware.item.name] += 1

    required_cyberware_numbers: Dict[str, int] = {}
    for required_cyberware in item.required_cyberware:
        required_cyberware_numbers.setdefault(required_cyberware, 0)
        required_cyberware_numbers[required_cyberware] += 1

    for required_cyberware_name, required_cyberware_numbers_num in required_cyberware_numbers.items():
        if required_cyberware_name in current_cyberware_numbers.keys():
            required_cyberware_numbers_num -= current_cyberware_numbers[required_cyberware_name]

        for _ in range(required_cyberware_numbers_num):
            logging.debug(left_align(f"{item} required a cyberware: {required_cyberware_name}, generating...", depth))

            required_cyberware_item: Item = next(
                cw for cw in all_cyberware if cw.name == required_cyberware_name).clone()

            required_cyberware_adding_result: Optional[CyberwareGenerationState] = add_cyberware(
                required_cyberware_item,
                replace(state, root=copy.deepcopy(state.root)),
                npc_template,
                all_cyberware,
                npc,
                depth + 1)

            if not required_cyberware_adding_result:
                logging.debug(left_align(f"Failed, couldn't create a required cyberware", depth))
                return None

            state = required_cyberware_adding_result
            logging.debug(left_align(f"Successfully created a required cyberware: {required_cyberware_item}", depth))

    container_selection_normalized_index: float = clamp(npc_template.rank.container_selection.generate(), 0.0, 1.0)
    logging.debug(left_align(f"Required container normalized index: {container_selection_normalized_index}", depth))

    # try to add this cyberware to an existing container
    container_where_added: Optional[InventoryNode] = None
    added_item: Optional[InventoryNode] = None
    for cyberware in state.root:
        added_item = add_to_container(item,
                                      cyberware,
                                      container_selection_normalized_index,
                                      npc,
                                      depth,
                                      first_pairing_container)
        if added_item:
            container_where_added = cyberware
            logging.debug(left_align(f"Found a suitable container: {container_where_added.item.name}", depth))
            break

    # try to buy the required containers
    if not container_where_added:
        logging.debug(left_align(f"Couldn't find a suitable container, trying to buy...", depth))
        for container in get_allowed_items(item.required_containers, container_selection_normalized_index):
            container_item: Item = next(cw for cw in all_cyberware if cw.name == container).clone()
            container_adding_result: Optional[CyberwareGenerationState] = add_cyberware(
                container_item,
                replace(state, root=copy.deepcopy(state.root)),
                npc_template,
                all_cyberware,
                npc,
                depth + 1)

            if container_adding_result:
                added_item = add_to_container(item,
                                              container_adding_result.last_added_cyberware,
                                              container_selection_normalized_index,
                                              npc,
                                              depth,
                                              first_pairing_container)
                if added_item:
                    state = container_adding_result
                    container_where_added = state.last_added_cyberware
                    break

    if not container_where_added:
        logging.debug(left_align(f"Couldn't create some of required containers", depth))
        return None

    assert added_item

    # create a paired container
    if item.must_be_paired and not container_where_added.item.paired_container:
        logging.debug(left_align(f"{item} required a paired item, generating...", depth))
        paired_container_adding_result: Optional[CyberwareGenerationState] = add_cyberware(
            create_paired_item(item),
            replace(state, root=copy.deepcopy(state.root)),
            npc_template,
            all_cyberware,
            npc,
            depth + 1,
            container_where_added)

        if not paired_container_adding_result:
            logging.debug(left_align(f"Failed, couldn't create a paired container", depth))
            return None

        state = paired_container_adding_result
        logging.debug(left_align(f"Successfully created a paired item: {state.last_added_cyberware.item}", depth))

    logging.debug(left_align(f"Found or created the all the required containers", depth))

    # decrease the money and the humanity
    if item.price > 0 and state.money_budget < item.price:
        logging.debug(left_align(
            f"Not enough money to buy this cyberware (required: {item.price}, available: {state.money_budget})",
            depth))
        return None
    state.money_budget -= item.price

    if item.max_humanity_loss > 0 and state.humanity_budget < item.max_humanity_loss:
        logging.debug(left_align(
            f"Not enough humanity to add this cyberware "
            f"(required: {item.max_humanity_loss}, available: {state.humanity_budget})",
            depth))
        return None
    state.humanity_budget -= item.max_humanity_loss

    state.last_added_cyberware = added_item

    logging.debug(f"\tAdded {added_item.item.name} to {container_where_added.item.name}")
    logging.debug(f"\t{state.money_budget=}")
    logging.debug(f"\t{state.humanity_budget=}")

    return state


def generate_cyberware(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating cyberware...")

    all_cyberware: List[Item] = list()
    for path in Path("configs/items/cyberware").glob('**/*.json'):
        data = load_data(str(path))
        all_cyberware += [dataclass_wizard.fromdict(Item, x) for x in data]

    cyberware_budget: int = round(npc_template.rank.items_budget[ItemType.CYBERWARE].generate())
    logging.debug(f"\t{cyberware_budget=}")

    logging.debug(f"\t{npc_template.role.min_empathy=}")
    humanity_budget: int = max(npc.stats[StatType.EMP] - npc_template.role.min_empathy, 0) * 10
    logging.debug(f"\t{humanity_budget=}")

    logging.debug(f"\t{npc_template.role.preferred_cyberware=}")

    npc.cyberware = InventoryNode(next(cw for cw in all_cyberware if cw.name == "Meatbody"))

    state = CyberwareGenerationState(None, npc.cyberware, cyberware_budget, humanity_budget)
    for i in range(RANDOM_GENERATING_NUM_ATTEMPTS):
        logging.debug(f"\n\tGenerating cyberware, attempt {i}")
        chosen_cyberware: str = choose_exponential_random_element(npc_template.role.preferred_cyberware)
        chosen_cyberware_item: Item = next(cw for cw in all_cyberware if cw.name == chosen_cyberware)
        cyberware_adding_result: Optional[CyberwareGenerationState] = add_cyberware(
            chosen_cyberware_item,
            replace(state, root=copy.deepcopy(state.root)),
            npc_template,
            all_cyberware,
            npc,
            1)

        if cyberware_adding_result:
            state = cyberware_adding_result

    npc.cyberware = state.root
    humanity_spent: int = humanity_budget - state.humanity_budget
    npc.stats[StatType.EMP] = math.floor((npc.stats[StatType.EMP] * 10 - humanity_spent) / 10)

    logging.debug(f"\n")
    logging.debug(f"\tHumanity left: {humanity_budget}")
    logging.debug(f"\tResulting EMP: {npc.stats[StatType.EMP]}")

    return npc
