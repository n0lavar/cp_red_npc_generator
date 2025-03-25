#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import math
from functools import cmp_to_key
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field, replace

from cp_red_npc_generator.src.utils import load_data
from npc_template import TraumaTeamStatusType
from modifier import ModifierSource
from inventory_node import InventoryNode
from item import Item, ItemType, ItemQuality
from stats import StatType, Skill, SkillType, StatSkillValue
from table_view import TableView


@dataclass
class Npc:
    stats: Dict[StatType, int] = field(default_factory=dict)
    skills: Dict[Skill, int] = field(default_factory=dict)
    cyberware: InventoryNode = field(default=None)
    armor: Set[Item] = field(default_factory=set)
    weapons: Set[Item] = field(default_factory=set)
    inventory: Dict[Item, int] = field(default_factory=dict)
    trauma_team_status: TraumaTeamStatusType = field(default=TraumaTeamStatusType.NONE)

    def get_all_items(self) -> List[Item]:
        equipped_items: List[Item] = copy.deepcopy(self.cyberware.get_all_items())
        equipped_items += [x for x in self.inventory.keys()]
        equipped_items += self.armor
        equipped_items += self.weapons

        return equipped_items

    def get_stat_or_skill_value(self, name: str) -> StatSkillValue:
        logging.debug(f"\tGetting a value and a modifier for {name}")

        equipped_items: List[Item] = self.get_all_items()

        def cmp_equipped_items_order(left: Item, right: Item) -> int:
            if (left.modifier_applying_priority < right.modifier_applying_priority
                    or left.creation_time < right.creation_time):
                return 1
            else:
                return -1

        equipped_items.sort(key=cmp_to_key(cmp_equipped_items_order))

        if name in [s.name for s in StatType] and StatType[name] in self.stats:
            start_value = self.stats[StatType[name]]
        else:
            start_value = next(level for skill, level in self.skills.items() if skill.name == name)

        modifier_value: int = 0
        modifiers: List[ModifierSource] = list()
        for item in equipped_items:
            for modifier in item.modifiers:
                new_modifier_value: int = modifier.apply(str(item), name, start_value, modifier_value)
                if new_modifier_value != modifier_value:
                    modifiers.append(ModifierSource(item.name, new_modifier_value - modifier_value))
                    modifier_value = new_modifier_value

        logging.debug(f"\t{name}: {start_value=}, {modifier_value=}")
        return StatSkillValue(start_value, modifier_value, modifiers)

    def get_skill_total_value(self, skill_name: str) -> int:
        skill: Skill = next(s for s in self.skills.keys() if s.name == skill_name)
        stat_value: int = self.get_stat_or_skill_value(skill.link.name).get_total()
        skill_value: int = self.get_stat_or_skill_value(skill_name).get_total()
        return stat_value + skill_value

    def to_string(self, flat: bool = False) -> str:
        logging.debug(f"\nConverting npc to a string...")

        all_items: List[Item] = self.get_all_items()
        stats_modifiers: Dict[StatType, StatSkillValue] = {}
        for stat in self.stats.keys():
            stats_modifiers[stat] = self.get_stat_or_skill_value(stat.name)

        npc_str: str = ""

        total_price = sum([x.price for x in all_items])
        npc_str += f"Has items total worth of {total_price}\n\n"

        stats_conditions_table_view = TableView(1 if flat else 4)

        conditions_rows: List[str] = list()

        max_hp = 10 + (5 * math.ceil(
            0.5 * (stats_modifiers[StatType.BODY].get_total() + stats_modifiers[StatType.WILL].get_total())))
        temp_str = f"    HP: {max_hp}/{max_hp} (Seriously Wounded: "
        if next((True for cw in self.cyberware if cw.item.name == "Pain Editor"), None):
            temp_str += f"No, Pain Editor"
        else:
            temp_str += f"{math.ceil(max_hp / 2)}"
        temp_str += ")"
        conditions_rows.append(temp_str)

        temp_str = f"    TraumaTeam status: {self.trauma_team_status.name}"
        conditions_rows.append(temp_str)

        can_evade_bullets_ref: bool = stats_modifiers[StatType.REF].get_total() >= 8
        can_evade_bullets_co_proc_ref: bool = bool(next(
            (cw for cw in self.cyberware if cw.item.name == "Reflex Co-Processor"), None))
        can_evade_bullets: bool = can_evade_bullets_ref or can_evade_bullets_co_proc_ref
        temp_str = f"    Can evade bullets: {can_evade_bullets}"
        if can_evade_bullets:
            temp_str += f" ("
            if can_evade_bullets_ref:
                temp_str += f"REF >= 8"
            elif can_evade_bullets_co_proc_ref:
                temp_str += f"Reflex Co-Processor"
            temp_str += f")"
        conditions_rows.append(temp_str)

        item_allowing_see_in_dark_smoke = next((i for i in all_items if "ImprovedVision" in i.unique_tags), None)
        temp_str = f"    No intangible obscurement penalties: {item_allowing_see_in_dark_smoke is not None}"
        if item_allowing_see_in_dark_smoke:
            temp_str += f" ({item_allowing_see_in_dark_smoke.name})"
        conditions_rows.append(temp_str)

        item_light_flashes_protection = next((i for i in all_items if "LightFlashesProtection" in i.unique_tags), None)
        temp_str = f"    Has flashes of light protection: {item_light_flashes_protection is not None}"
        if item_light_flashes_protection:
            temp_str += f" ({item_light_flashes_protection.name})"
        conditions_rows.append(temp_str)

        item_ears_protection = next((i for i in all_items if "EarsProtection" in i.unique_tags), None)
        temp_str = f"    Has ears protection: {item_ears_protection is not None}"
        if item_ears_protection:
            temp_str += f" ({item_ears_protection.name})"
        conditions_rows.append(temp_str)

        item_air_protection = next((i for i in all_items if "AirProtection" in i.unique_tags), None)
        temp_str = f"    Has breath protection: {item_air_protection is not None}"
        if item_air_protection:
            temp_str += f" ({item_air_protection.name})"
        conditions_rows.append(temp_str)

        stats_conditions_table_view.add(conditions_rows, "Conditions:", 1)

        stats_rows: List[str] = list()
        for stat in self.stats.keys():
            stat_value: StatSkillValue = stats_modifiers[stat]
            temp_str = f"    [{stat_value.value}"
            for stat_modifier in stat_value.modifiers:
                temp_str += f"{stat_modifier.value:+}({stat_modifier.item_name})"
            if stat_value.total_modifier != 0:
                temp_str += f"={stat_value.value + stat_value.total_modifier}"
            temp_str += f"] {stat.name}"
            stats_rows.append(temp_str)
        stats_conditions_table_view.add(stats_rows, "Stats:", 0)

        actions_rows: List[str] = [f"    {x.name}" for x in all_items if "Action" in x.get_all_tags()]
        stats_conditions_table_view.add(actions_rows, "Actions:", 2)

        abilities_rows: List[str] = [f"    {x.name}" for x in all_items if "Ability" in x.get_all_tags()]
        stats_conditions_table_view.add(abilities_rows, "Abilities:", 3)

        npc_str += str(stats_conditions_table_view)
        npc_str += "\n"

        npc_str += f"Skills:\n"
        skills_by_type = [[s for s in self.skills if s.type == t] for t in SkillType]
        skills_table_view = TableView(1 if flat else 3)
        for skills_of_one_type in skills_by_type:
            skills_of_one_type_rows: List[str] = [f"{skills_of_one_type[0].type.title()}"]

            for skill in skills_of_one_type:
                skill_value = self.get_stat_or_skill_value(skill.name)
                linked_stat_value = stats_modifiers[skill.link]
                skills_of_one_type_rows.append("    " + skill.to_string(linked_stat_value, skill_value))

            skills_table_view.add(skills_of_one_type_rows)
        npc_str += "    " + str(skills_table_view).replace("\n", "\n    ") + "\n"

        if len(self.cyberware.children):
            npc_str += f"Cyberware:\n"
            cyberware_table_view = TableView(1 if flat else 3)
            for basic_container in self.cyberware.children:
                cyberware_table_view.add(basic_container.to_string(0).removesuffix("\n").split("\n"))
            npc_str += "    " + str(cyberware_table_view).replace("\n", "\n    ") + "\n"

        if len(self.armor) or len(self.weapons):
            armor_weapon_table_view = TableView(1 if flat else 2)

            if len(self.armor):
                def armor_sorter(item: Item) -> int:
                    if item.name.startswith("Head"):
                        return 1
                    elif item.name.startswith("Body"):
                        return 2
                    elif "Shield" in item.name:
                        return 3
                    else:
                        return 4

                sorted_armor = sorted(self.armor, key=armor_sorter)
                armor_weapon_table_view.add(["    " + str(armor) for armor in sorted_armor], "Armor:", 0)

            if len(self.weapons):
                def weapon_sorter(item: Item) -> int:
                    return int(item.damage[0]) * int(item.damage[2]) * item.rate_of_fire

                weapon_skills_data: Dict[str, str] = load_data("configs/weapon_skills.json")

                def add_skill_value(weapon: Item) -> Item:
                    weapon_tags = weapon.get_all_tags()
                    skill_name: Optional[str] = None
                    if weapon.skill:
                        skill_name = weapon.skill
                    else:
                        for tag in weapon_tags:
                            if tag in weapon_skills_data.keys():
                                skill_name = weapon_skills_data[tag]
                                break

                    assert skill_name
                    skill_value: int = self.get_skill_total_value(skill_name)

                    additional_skill_value: Optional[int] = None
                    if "SMG" in weapon_tags or "HeavySMG" in weapon_tags or "AssaultRifle" in weapon_tags:
                        additional_skill_value = self.get_skill_total_value("Autofire")

                    if weapon.quality == ItemQuality.EXCELLENT:
                        skill_value += 1

                    if not additional_skill_value:
                        new_name: str = f"[{skill_value}] {weapon.name}"
                    else:
                        new_name: str = f"[{skill_value}(S)/{additional_skill_value}(A)] {weapon.name}"
                        
                    return replace(weapon, name=new_name)

                sorted_melee_weapon = sorted(
                    [add_skill_value(x) for x in self.weapons if "MeleeWeapon" in x.get_all_tags()],
                    key=weapon_sorter,
                    reverse=True)

                sorted_ranged_weapon = sorted(
                    [add_skill_value(x) for x in self.weapons if "RangedWeapon" in x.get_all_tags()],
                    key=weapon_sorter,
                    reverse=True)

                assert len(sorted_melee_weapon) + len(sorted_ranged_weapon) == len(self.weapons)

                armor_weapon_table_view.add(
                    ["    " + str(weapon) for weapon in sorted_ranged_weapon], "Ranged weapons:", 1)
                armor_weapon_table_view.add(
                    ["    " + str(weapon) for weapon in sorted_melee_weapon], "Melee weapons:", 1)

            npc_str += str(armor_weapon_table_view) + "\n"

        if len(self.inventory):
            npc_str += f"Inventory:\n"
            inventory_table_view = TableView(1 if flat else 3)

            def get_inventory_item_str(item: Item, amount: int) -> str:
                result: str = "    "
                if amount != 0:
                    result += f"[{amount}] "
                result += f"{item}"
                return result

            def add_table_view_part(name: str, types: List[ItemType], index: int):
                nonlocal inventory_table_view
                part_items: List[Tuple[Item, int]] = [(item, amount)
                                                      for item, amount in self.inventory.items()
                                                      if item.type in types]
                part_items.sort(key=lambda x: x[0].price * x[1], reverse=True)

                part: List[str] = [get_inventory_item_str(item, amount) for item, amount in part_items]
                inventory_table_view.add(part, name, index)

            add_table_view_part("Ammo", [ItemType.AMMO], 0)
            add_table_view_part("Equipment / Drugs", [ItemType.EQUIPMENT, ItemType.DRUG], 1)
            add_table_view_part("Junk", [ItemType.JUNK], 2)
            npc_str += "    " + str(inventory_table_view).replace("\n", "\n    ") + "\n"

        return npc_str

    def __str__(self):
        return self.to_string(False)
