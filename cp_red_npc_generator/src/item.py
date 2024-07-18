#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import time
from typing import List, Optional, Set
from dataclasses import dataclass, field, replace
from enum import StrEnum, auto

from modifier import Modifier
from price_category import PriceCategory


class ItemQuality(StrEnum):
    POOR = auto()
    STANDARD = auto()
    EXCELLENT = auto()


class ItemType(StrEnum):
    ARMOR = auto()
    WEAPON = auto()
    CYBERWARE = auto()
    AMMO = auto()
    EQUIPMENT = auto()
    DRUG = auto()
    JUNK = auto()


@dataclass(frozen=True, eq=True)
class Item:
    name: str = "Empty item"
    type: ItemType = ItemType.JUNK
    price: int = 0
    default_hidden: bool = False
    modifier_applying_priority: int = 0

    id: str = field(default=str(uuid.uuid4()), compare=False)
    creation_time: int = field(default=int(time.time_ns()), compare=False)

    tags: List[str] = field(default_factory=list, compare=False)
    modifiers: List[Modifier] = field(default_factory=list, compare=False)
    quality: Optional[ItemQuality] = field(default=None, compare=False)
    container_capacity: int = field(default=0, compare=False)
    size_in_container: int = field(default=0, compare=False)
    requires_container: List[str] = field(default_factory=list, compare=False)
    max_equipped_items: int = field(default=0, compare=False)  # 0 means inf

    # armor
    armor_class: Optional[int] = field(default=None, compare=False)

    # weapon
    damage: Optional[str] = field(default=None, compare=False)
    rate_of_fire: Optional[int] = field(default=None, compare=False)
    magazine: Optional[int] = field(default=None, compare=False)
    ammo_types: Set[str] = field(default_factory=set, compare=False)

    # cyberware
    max_humanity_loss: int = field(default=0, compare=False)
    must_be_paired: bool = field(default=False, compare=False)
    paired_container: bool = field(default=False, compare=False)
    required_cyberware: List[str] = field(default_factory=list, compare=False)
    required_condition: List[str] = field(default_factory=list, compare=False)  # Python code

    def clone(self, *args, **kwargs):
        return replace(self, id=str(uuid.uuid4()), creation_time=int(time.time_ns()), *args, **kwargs)

    def contains_any_tag_from(self, item) -> bool:
        for tag1 in self.tags:
            for tag2 in item.tags:
                if tag1 == tag2:
                    return True

        return False

    def to_string(self, short: bool = False) -> str:
        value: str = f"{self.name}"
        info: str = " ["
        if self.price > 0:
            info += f"{self.price}eb"
            if not short:
                info += f" ({PriceCategory.from_price(self.price).name.lower()})"
            info += f", "

        if not short:
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
            # if logging.root.isEnabledFor(logging.DEBUG):
            #    info += f"id={self.id}, "

        if len(info) > 2:
            info = info.removesuffix(", ")
            info += "]"
        else:
            info = ""

        return f"{value}{info}"

    def __str__(self):
        return self.to_string(False)
