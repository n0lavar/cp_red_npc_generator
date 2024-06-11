#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum, auto


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


@dataclass(frozen=True, eq=True)
class Skill:
    name: str = "Empty skill"
    link: StatType = StatType.INT
    type: SkillType = SkillType.EDUCATION

    def to_string(self, skill_value, skill_modifier, stat_value, stat_modifier) -> str:
        result: str = ""
        linked_stat_value = stat_value + stat_modifier
        result += f"[{linked_stat_value}{skill_value:+}{skill_modifier:+}"
        result += f"={linked_stat_value + skill_value + skill_modifier}] {self.name}"
        return result

    def __lt__(self, other):
        return self.name < other.name
