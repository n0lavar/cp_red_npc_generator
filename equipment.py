#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import dataclass_wizard

from data import *


def generate_cyberware(npc: Npc, npc_template: NpcTemplate) -> Npc:
    return npc


def generate_armor(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating armor...")
    with open("Configs/items/armor.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        all_armor: List[Item] = sorted([dataclass_wizard.fromdict(Item, x) for x in data],
                                       key=lambda x: x.cost,
                                       reverse=True)

        total_budget: int = round(npc_template.rank.items_budget[ItemType("armor")].generate())
        logging.debug(f"\t{total_budget=}")

        body_armor_budget: int = round(total_budget * 0.8)
        logging.debug(f"\t{body_armor_budget=}")

        head_armor_budget: int = round(total_budget * 0.2)
        logging.debug(f"\t{head_armor_budget=}")

        logging.debug(f"\t{npc_template.role.preferred_armor_class=}")

        def pick_armor(budget: int, preferred_armor_class: int) -> Optional[Item]:
            nonlocal all_armor
            for armor in all_armor:
                if armor.cost > budget:
                    continue
                if armor.armor_class > preferred_armor_class:
                    continue
                return armor

            return None

        npc.armor_body = pick_armor(body_armor_budget, npc_template.role.preferred_armor_class)
        logging.debug(f"\tPicked: npc.armor_body={npc.armor_body}")
        npc.armor_head = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class)
        logging.debug(f"\tPicked: npc.armor_head={npc.armor_head}")

    return npc


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    return npc


def generate_ammo(npc: Npc, npc_template: NpcTemplate) -> Npc:
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
