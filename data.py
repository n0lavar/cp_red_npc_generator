#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import StrEnum, auto

from normal_distribution import NormalDistribution


class ItemType(StrEnum):
    ARMOR = auto()
    WEAPON = auto()
    CYBERWARE = auto()
    AMMO = auto()
    EQUIPMENT = auto()
    JUNK = auto()


class GangType(StrEnum):
    # core book gangs
    THE_BOZOS = auto()
    INQUISITORS = auto()
    IRON_SIGHTS = auto()
    MAELSTROM = auto()
    PHILHARMONIC_VAMPIRES = auto()
    PIRANHAS = auto()
    THE_PRIME_TIME_PLAYERS = auto()
    RECKONERS = auto()
    RED_CHROME_LEGION = auto()
    SCAVVERS = auto()
    STEEL_VAQUEROS = auto()
    TYGER_CLOWS = auto()
    VOODOO_BOYS = auto()
    # some additional gangs based on info from the core book
    ARASAKA = auto()
    MILITECH = auto()
    TRAUMA_TEAM = auto()
    POLICE = auto()
    MAX_TAC = auto()
    # "general" gangs
    CORP = auto()
    EDGERUNNERS = auto()
    BOOSTERS = auto()


class SkillType(StrEnum):
    AWARENESS = auto()
    BODY = auto()
    CONTROL = auto()
    EDUCATION = auto()
    FIGHTING = auto()
    PERFORMANCE = auto()
    RANGED_WEAPON = auto()
    SOCIAL = auto()
    TECHNIQUE = auto()


class StatType(StrEnum):
    INT = auto()
    REF = auto()
    DEX = auto()
    TECH = auto()
    COOL = auto()
    WILL = auto()
    LUCK = auto()
    MOVE = auto()
    BODY = auto()
    EMP = auto()


def stat_type_from_int(i: int) -> StatType:
    match i:
        case 0:
            return StatType.INT
        case 1:
            return StatType.REF
        case 2:
            return StatType.DEX
        case 3:
            return StatType.TECH
        case 4:
            return StatType.COOL
        case 5:
            return StatType.WILL
        case 6:
            return StatType.LUCK
        case 7:
            return StatType.MOVE
        case 8:
            return StatType.BODY
        case 9:
            return StatType.EMP


@dataclass
class Rank:
    name: str = "Empty rank"
    items_budget: Dict[ItemType, NormalDistribution] = field(default_factory=dict)
    stats_budget: NormalDistribution = field(default_factory=NormalDistribution)
    skills_budget: NormalDistribution = field(default_factory=NormalDistribution)
    exp_budget: NormalDistribution = field(default_factory=NormalDistribution)

    @staticmethod
    def load():
        with open("Configs/ranks.json", "r", encoding="utf-8") as f:
            return json.load(f)


@dataclass(frozen=True, eq=True)
class Role:
    name: str

    preferred_cyberware: List[str] = field(default_factory=list, compare=False)
    preferred_weapons: List[str] = field(default_factory=list, compare=False)
    # npc won't try to buy armor with a greater armor class
    preferred_armor_class: int = field(default=11, compare=False)

    @staticmethod
    def load():
        with open("Configs/roles.json", "r", encoding="utf-8") as f:
            return json.load(f)


@dataclass(frozen=True, eq=True)
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION

    def __str__(self):
        return f"[{self.link}] {self.name}"


@dataclass
class Modifier:
    name: str = "Empty modifier"
    value: int = 0


@dataclass
class Item:
    name: str = "Empty item"
    type: ItemType = ItemType.JUNK
    cost: int = 0

    modifiers: List[Modifier] = field(default_factory=list, compare=False)
    armor_class: Optional[int] = field(default=None, compare=False)

    def __str__(self):
        value: str = f"{self.name} ({self.cost}eb"
        if self.armor_class:
            value += f", SP={self.armor_class}"
        value += ")"
        return value


@dataclass
class NpcTemplate:
    rank: Rank = field(default_factory=Rank)
    gang: GangType = GangType.BOOSTERS
    role: Role = field(default_factory=Role)


@dataclass
class Npc:
    stats: Dict[StatType, int] = field(default_factory=dict)
    skills: Dict[Skill, int] = field(default_factory=dict)
    cyberware: List[Item] = field(default_factory=list)
    armor_head: Item = field(default_factory=Item)
    armor_body: Item = field(default_factory=Item)
    primary_weapon: Item = field(default_factory=Item)
    secondary_weapon: Item = field(default_factory=Item)
    inventory: Dict[Item, int] = field(default_factory=dict)

    def get_equipped_items(self) -> List[Item]:
        """returns items that may have modifiers"""
        return self.cyberware + [self.armor_head, self.armor_body, self.primary_weapon, self.secondary_weapon]

    def get_stat_or_skill_value(self, name: str) -> Tuple[int, int]:
        equipped_items: List[Item] = self.get_equipped_items()

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

        npc_str += f"Stats: (stat + modifiers)\n"
        for stat in self.stats.keys():
            stat_value, stat_modifier = self.get_stat_or_skill_value(stat.name)
            npc_str += f"\t[{stat_value}"
            if stat_modifier != 0:
                npc_str += f"{stat_modifier:+}={stat_value + stat_modifier}"
            npc_str += f"] {stat.name}\n"

        npc_str += f"\nSkills (stat + skill + modifiers):\n"
        for skill in self.skills.keys():
            skill_value, skill_modifier = self.get_stat_or_skill_value(skill.name)
            stat_value, stat_modifier = self.get_stat_or_skill_value(str(skill.link))
            linked_stat_value = stat_value + stat_modifier
            npc_str += f"\t[{linked_stat_value}+{skill_value}"
            if skill_modifier != 0:
                npc_str += f"{skill_modifier:+}"
            npc_str += f"={skill_value + linked_stat_value + skill_modifier}] {skill.name}\n"

        npc_str += f"\nArmor:\n"
        npc_str += f"\t{self.armor_head}\n"
        npc_str += f"\t{self.armor_body}\n"

        return npc_str
