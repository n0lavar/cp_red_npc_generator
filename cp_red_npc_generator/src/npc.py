#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import math
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, field

from item import Item, ItemType
from stats import StatType, Skill, SkillType
from utils import left_align
from table_view import TableView


@dataclass
class InventoryNode:
    item: Item = field(default=Item)
    children: List = field(default_factory=list)

    def can_add_child(self, child: Item) -> bool:
        node_capacity: int = self.item.container_capacity
        node_size: int = sum([x.item.size_in_container for x in self.children])
        if node_size + child.size_in_container > node_capacity:
            return False

        if self.item.name not in child.requires_container:
            return False

        return True

    def add_child(self, child: Item):  # -> Optional[InventoryNode]:
        if self.can_add_child(child):
            # new_node = InventoryNode(replace(copy.deepcopy(child), id=str(uuid.uuid4())))
            # new_node = InventoryNode(copy.deepcopy(child))
            new_node = InventoryNode(child.clone())
            self.children.append(new_node)
            return new_node
        else:
            return None

    def get_all_items(self) -> List[Item]:
        items: List[Item] = [self.item]
        for inventory_node in self.children:
            items += inventory_node.get_all_items()

        return items

    def __iter__(self):
        return self._traverse(self)

    def _traverse(self, node):
        yield node
        for child in node.children:
            yield from self._traverse(child)

    def to_string(self, offset: int) -> str:
        if self.item.default_hidden and len(self.children) == 0:
            return ""

        result: str = left_align(f"{self.item.to_string(True)}", offset, "    ")

        if self.item.container_capacity != 0 and self.item.container_capacity < 100:
            result += f" [{sum([x.item.size_in_container for x in self.children])}/{self.item.container_capacity}]"

        result += "\n"

        for child in self.children:
            result += child.to_string(offset + 1)

        return result


@dataclass
class Npc:
    stats: Dict[StatType, int] = field(default_factory=dict)
    skills: Dict[Skill, int] = field(default_factory=dict)
    cyberware: InventoryNode = field(default=None)
    armor: Set[Item] = field(default_factory=set)
    weapons: Set[Item] = field(default_factory=set)
    inventory: Dict[Item, int] = field(default_factory=dict)

    def get_all_items(self) -> List[Item]:
        equipped_items: List[Item] = copy.deepcopy(self.cyberware.get_all_items())
        equipped_items += [x for x in self.inventory.keys()]
        equipped_items += self.armor
        equipped_items += self.weapons

        return equipped_items

    def get_stat_or_skill_value(self, name: str) -> Tuple[int, int]:
        logging.debug(f"\tGetting a value and a modifier for {name}")

        equipped_items: List[Item] = self.get_all_items()
        equipped_items.sort(key=lambda x: x.creation_time)

        if name.lower() in StatType and StatType(name.lower()) in self.stats:
            start_value = self.stats[StatType(name.lower())]
        else:
            start_value = next(level for skill, level in self.skills.items() if skill.name == name)

        modifier_value: int = 0
        for item in equipped_items:
            for modifier in item.modifiers:
                modifier_value = modifier.apply(str(item), name, start_value, modifier_value)

        logging.debug(f"\t{name}: {start_value=}, {modifier_value=}")
        return start_value, modifier_value

    def to_string(self, flat: bool = False) -> str:
        logging.debug(f"\nConverting npc to a string...")

        npc_str: str = ""

        total_price = sum([x.price for x in self.get_all_items()])
        npc_str += f"Has items total worth of {total_price}\n\n"

        max_hp = 10 + (5 * math.ceil(0.5 * (self.stats[StatType.BODY] + self.stats[StatType.COOL])))
        npc_str += f"Health (you can add conditions here):\n"
        npc_str += f"\tHP: {max_hp}/{max_hp} (Seriously Wounded: "
        if next((True for cw in self.cyberware if cw.item.name == "Pain Editor"), None):
            npc_str += f"No, Pain Editor"
        else:
            npc_str += f"{math.ceil(max_hp / 2)}"
        npc_str += ")\n\n"

        npc_str += f"Stats: (stat+modifiers=total)\n\t"
        stats_modifiers: Dict[StatType, Tuple[int, int]] = {}
        for stat in self.stats.keys():
            stat_value, stat_modifier = self.get_stat_or_skill_value(stat.name)
            stats_modifiers[stat] = stat_value, stat_modifier
            npc_str += f"[{stat_value}"
            if stat_modifier != 0:
                npc_str += f"{stat_modifier:+}={stat_value + stat_modifier}"
            npc_str += f"] {stat.name} | "
        npc_str = npc_str.removesuffix(" | ") + "\n\n"

        npc_str += f"Skills (stat+skill+modifiers=total):\n"
        skills_by_type = [[s for s in self.skills if s.type == t] for t in SkillType]
        skills_table_view = TableView(1 if flat else 4)
        for skills_of_one_type in skills_by_type:
            skills_of_one_type_rows: List[str] = [f"{skills_of_one_type[0].type.title()}"]

            for skill in skills_of_one_type:
                skill_value, skill_modifier = self.get_stat_or_skill_value(skill.name)
                stat_value, stat_modifier = stats_modifiers[skill.link]
                skills_of_one_type_rows.append(
                    "    " + skill.to_string(skill_value, skill_modifier, stat_value, stat_modifier))

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

                sorted_melee_weapon = sorted([x for x in self.weapons if "MeleeWeapon" in x.tags],
                                             key=weapon_sorter,
                                             reverse=True)

                sorted_ranged_weapon = sorted(list(set(self.weapons) - set(sorted_melee_weapon)),
                                              key=weapon_sorter,
                                              reverse=True)

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
