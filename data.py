#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict, List
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


class RoleType(StrEnum):
    # core book roles
    ROCKERBOY = auto()
    SOLO = auto()
    NETRUNNER = auto()
    TECH = auto()
    MEDTECH = auto()
    MEDIA = auto()
    EXEC = auto()
    LAWMAN = auto()
    FIXER = auto()
    NOMAD = auto()
    # "general" roles
    CIVILIAN = auto()
    BOOSTER = auto()


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


@dataclass(frozen=True, eq=True)
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION

    def __str__(self):
        return f"[{self.link}] {self.name}"


@dataclass
class Item:
    name: str = "Empty item"
    type: ItemType = ItemType.JUNK
    cost: int = 0

    def __str__(self):
        return f"[{self.type}] {self.name} ({self.cost}eb)"


@dataclass
class NpcTemplate:
    rank: Rank = field(default_factory=Rank)
    gang: GangType = GangType.BOOSTERS
    role: RoleType = RoleType.BOOSTER


@dataclass
class Npc:
    stats: Dict[StatType, int] = field(default_factory=dict)
    skills: Dict[Skill, int] = field(default_factory=dict)
    armor_head: Item = field(default_factory=Item)
    armor_body: Item = field(default_factory=Item)
    cyberware: List[Item] = field(default_factory=list)
    primary_weapon: Item = field(default_factory=Item)
    secondary_weapon: Item = field(default_factory=Item)
    inventory: Dict[Item, int] = field(default_factory=dict)

    def __str__(self):
        npc_str: str = ""

        npc_str += f"Stats:\n"
        for stat, level in self.stats.items():
            npc_str += f"\t[{level}] {stat}\n"

        npc_str += f"\nSkills (stat + skill + modifiers):\n"
        for skill, level in self.skills.items():
            npc_str += f"\t[{self.stats[skill.link]}+{level}={level + self.stats[skill.link]}] {skill.name}\n"

        return npc_str
