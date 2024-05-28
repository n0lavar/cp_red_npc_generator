#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Dict, List, Set
from dataclasses import dataclass, field

from item import ItemQuality, ItemType
from normal_distribution import NormalDistribution
from utils import load_data


@dataclass
class Rank:
    name: str = "Empty rank"
    min_items_quality: ItemQuality = field(default=ItemQuality.POOR)
    items_budget: Dict[ItemType, NormalDistribution] = field(default_factory=dict)
    items_num_budget: Dict[ItemType, NormalDistribution] = field(default_factory=dict)
    stats_budget: NormalDistribution = field(default_factory=NormalDistribution)
    skills_budget: NormalDistribution = field(default_factory=NormalDistribution)
    exp_budget: NormalDistribution = field(default_factory=NormalDistribution)

    @staticmethod
    def load():
        return load_data("Configs/ranks.json")


@dataclass(frozen=True, eq=True)
class Role:
    name: str

    preferred_cyberware: List[str] = field(default_factory=list, compare=False)
    preferred_primary_weapons: Set[str] = field(default_factory=set, compare=False)
    preferred_secondary_weapons: Set[str] = field(default_factory=set, compare=False)
    preferred_ammo: List[str] = field(default_factory=list, compare=False)
    # npc won't try to buy armor with a greater armor class
    preferred_armor_class: int = field(default=11, compare=False)
    preferred_drugs: List[str] = field(default_factory=list, compare=False)
    preferred_equipment: List[str] = field(default_factory=list, compare=False)

    @staticmethod
    def load():
        return load_data("Configs/roles.json")


@dataclass
class NpcTemplate:
    rank: Rank = field(default_factory=Rank)
    role: Role = field(default_factory=Role)
