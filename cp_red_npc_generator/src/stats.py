#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, Enum
from typing import List

from modifier import ModifierSource


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


class StatType(Enum):
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
class StatSkillValue:
    value: int = 0
    total_modifier: int = 0
    modifiers: List[ModifierSource] = field(default_factory=list)

    def get_total(self) -> int:
        return self.value + self.total_modifier


@dataclass(frozen=True, eq=True)
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION

    def to_string(self, linked_stat_value: StatSkillValue, skill_value: StatSkillValue) -> str:
        result: str = "["
        result += f"{linked_stat_value.get_total()}({self.link.name})"
        if skill_value.value > 0:
            result += f"{skill_value.value:+}"
        for skill_modifier in skill_value.modifiers:
            result += f"{skill_modifier.value:+}({skill_modifier.item_name})"
        result += f"={linked_stat_value.get_total() + skill_value.get_total()}] {self.name}"
        return result

    def __lt__(self, other):
        return self.name < other.name
