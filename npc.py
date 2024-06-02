#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import math
from typing import Dict, List, Optional, Tuple, Callable, Set
from dataclasses import dataclass, field

from item import Item, ItemType
from stats import StatType, Skill
from utils import left_align


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
            new_node = InventoryNode(copy.deepcopy(child))
            self.children.append(new_node)
            return new_node
        else:
            return None

    def get_all_items(self) -> Set[Item]:
        items: Set[Item] = {self.item}
        for inventory_node in self.children:
            items.update(inventory_node.get_all_items())

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

        result: str = left_align(f"{self.item}", offset)

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
    armor_head: Optional[Item] = field(default=None)
    armor_body: Optional[Item] = field(default=None)
    weapons: Set[Item] = field(default_factory=set)
    inventory: Dict[Item, int] = field(default_factory=dict)

    def get_all_items(self) -> Set[Item]:
        equipped_items: Set[Item] = copy.deepcopy(self.cyberware.get_all_items())
        equipped_items.update([x for x in self.inventory.keys()])
        if self.armor_head:
            equipped_items.add(self.armor_head)
        if self.armor_body:
            equipped_items.add(self.armor_body)

        equipped_items.update(self.weapons)

        return equipped_items

    def get_stat_or_skill_value(self, name: str) -> Tuple[int, int]:
        equipped_items: Set[Item] = self.get_all_items()

        if name.lower() in StatType and StatType(name.lower()) in self.stats:
            value = self.stats[StatType(name.lower())]
        else:
            value = next(level for skill, level in self.skills.items() if skill.name == name)

        modifier_value: int = 0
        for item in equipped_items:
            for modifier in item.modifiers:
                if name.lower() == modifier.name.lower():
                    modifier_value += modifier.value

        return value, modifier_value

    def __str__(self):
        npc_str: str = ""

        total_price = sum([x.price for x in self.get_all_items()])
        npc_str += f"Has items total worth of {total_price}\n\n"

        max_hp = 10 + (5 * math.ceil(0.5 * (self.stats[StatType.BODY] + self.stats[StatType.COOL])))
        npc_str += f"Health (you can add conditions here):\n"
        npc_str += f"\tHP: {max_hp}/{max_hp} (Seriously Wounded: {math.ceil(max_hp / 2)})\n\n"

        npc_str += f"Stats: (stat + modifiers)\n\t"
        for stat in self.stats.keys():
            stat_value, stat_modifier = self.get_stat_or_skill_value(stat.name)
            npc_str += f"[{stat_value}"
            if stat_modifier != 0:
                npc_str += f"{stat_modifier:+}={stat_value + stat_modifier}"
            npc_str += f"] {stat.name} | "
        npc_str = npc_str.removesuffix(" | ") + "\n"

        npc_str += f"\nSkills (stat + skill + modifiers):\n"

        types = set(map(lambda s: s.type, self.skills.keys()))
        skills_by_type = [[s for s in self.skills if s.type == t] for t in types]
        for skills_of_one_type in skills_by_type:
            if len(skills_of_one_type) > 0:
                npc_str += f"\t{skills_of_one_type[0].type.title()}\n"

            for skill in skills_of_one_type:
                skill_value, skill_modifier = self.get_stat_or_skill_value(skill.name)
                stat_value, stat_modifier = self.get_stat_or_skill_value(str(skill.link))
                linked_stat_value = stat_value + stat_modifier
                npc_str += f"\t\t[{linked_stat_value}+{skill_value}"
                if skill_modifier != 0:
                    npc_str += f"{skill_modifier:+}"
                npc_str += f"={skill_value + linked_stat_value + skill_modifier}] {skill.name}\n"

        npc_str += f"\nCyberware:\n"
        for basic_container in self.cyberware.children:
            npc_str += basic_container.to_string(1)

        npc_str += f"\nArmor:\n"
        if self.armor_head:
            npc_str += f"\tHead: {self.armor_head}\n"
        if self.armor_body:
            npc_str += f"\tBody: {self.armor_body}\n"

        if len(self.weapons):
            npc_str += f"\nWeapons:\n"
        for weapon in self.weapons:
            npc_str += f"\t{weapon}\n"

        if len(self.inventory):
            npc_str += f"\nInventory:\n"
        for item, amount in self.inventory.items():
            npc_str += "\t"
            if amount != 0:
                npc_str += f"[{amount}] "
            npc_str += f"{item}\n"

        return npc_str
