#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import logging
import dataclass_wizard
import random

from data import *


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

        head_armor_budget: int = total_armor_budget - npc.armor_body.price if npc.armor_body else total_armor_budget
        logging.debug(f"\t{head_armor_budget=}")
        npc.armor_head = pick_armor(head_armor_budget, npc_template.role.preferred_armor_class)

        logging.debug(f"\tPicked: npc.armor_body={npc.armor_body}")
        logging.debug(f"\tPicked: npc.armor_head={npc.armor_head}")

    return npc


def generate_weapon(npc: Npc, npc_template: NpcTemplate) -> Npc:
    logging.debug("\nGenerating weapons...")
    with open("Configs/items/weapon.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        @dataclass
        class ItemWithNames(Item):
            possible_names: List[str] = field(default_factory=list)

            def pick_name(self):
                if self.possible_names:
                    self.name = f"{random.choice(self.possible_names)} ({self.name})"

        all_weapons: List[ItemWithNames] = [dataclass_wizard.fromdict(ItemWithNames, x) for x in data]

        def pick_weapon(budget: int, preferred_weapons: List[str]) -> Optional[Item]:
            nonlocal npc_template, all_weapons

            max_attempts: int = 100
            for attempt in range(max_attempts):
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

                preferred_weapon: str = random.choice(preferred_weapons)
                preferred_weapon_item: ItemWithNames = copy.deepcopy(
                    next(w for w in all_weapons if w.name == preferred_weapon))
                preferred_quality: ItemQuality = random.choice(preferred_qualities)
                initial_price_category: PriceCategory = price_category_from_price(preferred_weapon_item.price)
                match preferred_quality:
                    case ItemQuality.POOR:
                        if initial_price_category.value - 1 not in PriceCategory:
                            continue
                        preferred_weapon_item.price = PriceCategory(initial_price_category.value - 1).get_price()
                    case ItemQuality.EXCELLENT:
                        if initial_price_category.value + 1 not in PriceCategory:
                            continue
                        preferred_weapon_item.price = PriceCategory(initial_price_category.value + 1).get_price()

                if preferred_weapon_item.price <= budget:
                    preferred_weapon_item.pick_name()
                    preferred_weapon_item.quality = preferred_quality
                    return preferred_weapon_item

            return None

        total_weapons_budget: int = round(npc_template.rank.items_budget[ItemType("weapon")].generate())
        logging.debug(f"\t{total_weapons_budget=}")

        primary_weapon_budget: int = round(total_weapons_budget * 0.8)
        logging.debug(f"\t{primary_weapon_budget=}")
        npc.primary_weapon = pick_weapon(primary_weapon_budget, npc_template.role.preferred_primary_weapons)

        secondary_weapon_budget: int = total_weapons_budget - npc.primary_weapon.price if npc.primary_weapon else total_weapons_budget
        logging.debug(f"\t{secondary_weapon_budget=}")
        npc.secondary_weapon = pick_weapon(secondary_weapon_budget, npc_template.role.preferred_secondary_weapons)

        logging.debug(f"\tPicked: npc.primary_weapon={npc.primary_weapon}")
        logging.debug(f"\tPicked: npc.secondary_weapon={npc.secondary_weapon}")

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
