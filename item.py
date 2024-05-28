#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Optional, Set
from dataclasses import dataclass, field
from enum import StrEnum, auto, Enum


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
    DRUG = auto()
    JUNK = auto()


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
    container_capacity: int = field(default=0, compare=False)
    size_in_container: int = field(default=0, compare=False)
    requires_container: List[str] = field(default_factory=list, compare=False)

    # armor
    armor_class: Optional[int] = field(default=None, compare=False)

    # weapon
    damage: Optional[str] = field(default=None, compare=False)
    rate_of_fire: Optional[int] = field(default=None, compare=False)
    magazine: Optional[int] = field(default=None, compare=False)
    ammo_types: Set[str] = field(default_factory=set, compare=False)

    # cyberware
    max_humanity_loss: int = field(default=0, compare=False)

    def __str__(self):
        value: str = f"{self.name}"
        info: str = " ["
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
            info += f"Mag=/{self.magazine} (), "

        if len(info) > 2:
            info = info.removesuffix(", ")
            info += "]"
        else:
            info = ""

        return f"{value}{info}"
