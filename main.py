#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from typing import Dict, List
import argparse
from dataclasses import dataclass, fields, field
from enum import StrEnum, auto
import dataclass_wizard


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


@dataclass
class NormalDistribution:
    mean: float = 0
    standard_deviation: float = 0


@dataclass
class Rank:
    name: str = "Empty rank"
    items_budget: Dict[ItemType, NormalDistribution] = field(default_factory=dict)
    exp_budget: NormalDistribution = field(default_factory=NormalDistribution)


@dataclass
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION
    exp_cost: List[int] = field(default_factory=list)


@dataclass
class Item:
    name: str = "Empty item"
    type: ItemType = ItemType.JUNK
    cost: int = 0


@dataclass
class NpcTemplate:
    rank: Rank = field(default_factory=Rank)
    gang: GangType = GangType.BOOSTERS
    role: RoleType = RoleType.BOOSTER


@dataclass
class Npc:
    name: str = ""
    description: str = ""
    stats: Dict[StatType, int] = field(default_factory=dict)
    skills: Dict[Skill, int] = field(default_factory=dict)
    armor_head: Item = field(default_factory=Item)
    armor_body: Item = field(default_factory=Item)
    cyberware: List[Item] = field(default_factory=list)
    primary_weapon: Item = field(default_factory=Item)
    secondary_weapon: Item = field(default_factory=Item)
    inventory: Dict[Item, int] = field(default_factory=dict)


def create_npc(npc_template: NpcTemplate) -> Npc:
    npc = Npc()
    return npc


def main(args) -> int:
    with open("Configs/ranks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        rank = dataclass_wizard.fromdict(Rank, next(n for n in data if n["name"] == args.rank))
        print(rank)

    npc = create_npc(NpcTemplate(rank, GangType(args.gang), RoleType(args.role)))
    print(npc)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=str, required=True)
    parser.add_argument("--role", type=str, required=True)
    parser.add_argument("--gang", type=str, required=True)

    return_code = main(parser.parse_args())
    exit(return_code)
