#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import json
import math
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import StrEnum, auto, Enum

from normal_distribution import NormalDistribution


class ItemQuality(StrEnum):
    POOR = auto()
    STANDARD = auto()
    EXCELLENT = auto()


class PriceCategory(Enum):
    CHEAP = 0
    EVERYDAY = 1
    COSTLY = 2
    PREMIUM = 3
    EXPENSIVE = 4
    VERY_EXPENSIVE = 5
    LUXURY = 6
    SUPER_LUXURY = 7

    def get_price(self) -> int:
        match self:
            case PriceCategory.CHEAP:
                return 10
            case PriceCategory.EVERYDAY:
                return 20
            case PriceCategory.COSTLY:
                return 50
            case PriceCategory.PREMIUM:
                return 100
            case PriceCategory.EXPENSIVE:
                return 500
            case PriceCategory.VERY_EXPENSIVE:
                return 1000
            case PriceCategory.LUXURY:
                return 5000
            case PriceCategory.SUPER_LUXURY:
                return 10000


def price_category_from_price(price: int):
    if price <= 10:
        return PriceCategory.CHEAP
    elif price <= 20:
        return PriceCategory.EVERYDAY
    elif price <= 50:
        return PriceCategory.COSTLY
    elif price <= 100:
        return PriceCategory.PREMIUM
    elif price <= 500:
        return PriceCategory.EXPENSIVE
    elif price <= 1000:
        return PriceCategory.VERY_EXPENSIVE
    elif price <= 5000:
        return PriceCategory.LUXURY
    else:
        return PriceCategory.SUPER_LUXURY


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
    min_items_quality: ItemQuality = field(default=ItemQuality.POOR)
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
    preferred_primary_weapons: Set[str] = field(default_factory=set, compare=False)
    preferred_secondary_weapons: Set[str] = field(default_factory=set, compare=False)
    preferred_ammo: List[str] = field(default_factory=list, compare=False)
    # npc won't try to buy armor with a greater armor class
    preferred_armor_class: int = field(default=11, compare=False)
    preferred_equipment: List[str] = field(default_factory=list, compare=False)

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


@dataclass(frozen=True, eq=True)
class Item:
    name: str = "Empty item"
    type: ItemType = ItemType.JUNK
    price: int = 0
    modifiers: List[Modifier] = field(default_factory=list, compare=False)
    quality: Optional[ItemQuality] = field(default=None, compare=False)

    armor_class: Optional[int] = field(default=None, compare=False)

    damage: Optional[str] = field(default=None, compare=False)
    rate_of_fire: Optional[int] = field(default=None, compare=False)
    magazine: Optional[int] = field(default=None, compare=False)
    ammo_types: Set[str] = field(default_factory=set, compare=False)

    def __str__(self):
        value: str = f"{self.name}"
        info: str = "["
        if self.price > 0:
            info += f"{self.price}eb ({price_category_from_price(self.price).name.lower()}), "
        if self.armor_class:
            info += f"SP={self.armor_class}/{self.armor_class}, "
        if self.quality:
            info += f"{self.quality}, "
        if self.damage:
            info += f"Damage={self.damage}, "
        if self.rate_of_fire:
            info += f"ROF={self.rate_of_fire}, "
        if self.magazine:
            info += f"Mag=0/{self.magazine}, "
        if len(info) > 1:
            info = info.removesuffix(", ")
            info += "]"
        else:
            info = ""
        return f"{value} {info}"


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
    armor_head: Optional[Item] = field(default=None)
    armor_body: Optional[Item] = field(default=None)
    primary_weapon: Optional[Item] = field(default=None)
    secondary_weapon: Optional[Item] = field(default=None)
    inventory: Dict[Item, int] = field(default_factory=dict)

    def get_all_items(self) -> List[Item]:
        equipped_items: List[Item] = copy.deepcopy(self.cyberware)
        equipped_items += [x for x in self.inventory.keys()]
        if self.armor_head:
            equipped_items.append(self.armor_head)
        if self.armor_body:
            equipped_items.append(self.armor_body)
        if self.primary_weapon:
            equipped_items.append(self.primary_weapon)
        if self.secondary_weapon:
            equipped_items.append(self.secondary_weapon)

        return equipped_items

    def get_stat_or_skill_value(self, name: str) -> Tuple[int, int]:
        equipped_items: List[Item] = self.get_all_items()

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
        npc_str += f"Health:\n"
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

        npc_str += f"\nArmor:\n"
        if self.armor_head:
            npc_str += f"\tHead: {self.armor_head}\n"
        if self.armor_body:
            npc_str += f"\tBody: {self.armor_body}\n"

        npc_str += f"\nWeapons:\n"
        if self.primary_weapon:
            npc_str += f"\t{self.primary_weapon}\n"
        if self.secondary_weapon:
            npc_str += f"\t{self.secondary_weapon}\n"

        stat_value, stat_modifier = self.get_stat_or_skill_value(StatType.BODY.name)
        total_body = stat_value + stat_modifier

        if total_body <= 4:
            boxing_dmg = "1d6"
        elif total_body <= 6:
            boxing_dmg = "2d6"
        elif total_body <= 10:
            boxing_dmg = "3d6"
        else:
            boxing_dmg = "4d6"
        boxing: Item = Item(name="Boxing", type=ItemType.WEAPON, damage=boxing_dmg, rate_of_fire=1)
        npc_str += f"\t{boxing}\n"

        martial_arts_skill = next((s for s in self.skills if s.name == "MartialArts"), None)
        if martial_arts_skill:
            martial_arts: Item = Item(name="Martial Arts", type=ItemType.WEAPON, damage=boxing_dmg, rate_of_fire=2)
            npc_str += f"\t{martial_arts}\n"

        npc_str += f"\nInventory:\n"
        for item, amount in self.inventory.items():
            npc_str += "\t"
            if amount != 0:
                npc_str += f"[{amount}] "
            npc_str += f"{item}\n"

        return npc_str
