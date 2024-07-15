#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
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


@dataclass(frozen=True, eq=True)
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION

    def to_string(self,
                  skill_value: int,
                  skill_modifier_value: int,
                  stat_value: int,
                  stat_modifier_value: int,
                  skill_modifiers: List[ModifierSource]) -> str:
        linked_stat_value: int = stat_value + stat_modifier_value
        total_value: int = linked_stat_value + skill_value + skill_modifier_value
        result: str = "["
        result += f"{linked_stat_value}({self.link.name})"
        if skill_value > 0:
            result += f"{skill_value:+}"
        for skill_modifier in skill_modifiers:
            result += f"{skill_modifier.value:+}({skill_modifier.item_name})"
        result += f"={total_value}] {self.name}"
        return result

    def __lt__(self, other):
        return self.name < other.name
