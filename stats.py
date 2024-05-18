#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import json
import logging
from typing import Callable, Optional

from data import *


def clamp(n, min_value, max_value):
    if n < min_value:
        return min_value
    elif n > max_value:
        return max_value
    else:
        return n


def create_stats(npc: Npc, npc_template: NpcTemplate) -> Npc:
    def sort_and_modify(nums: List[int], modify_func: Callable[[int], Optional[int]]) -> List[int]:
        indexed_nums = list(enumerate(nums))
        sorted_indexed_nums = sorted(indexed_nums, key=lambda x: x[1], reverse=True)

        def apply_modify_func(values):
            changes_made = True
            while changes_made:
                changes_made = False
                for i in range(len(values)):
                    original_value = values[i][1]
                    new_value = modify_func(original_value)
                    if new_value is not None and new_value != original_value:
                        values[i] = (values[i][0], new_value)
                        changes_made = True
            return values

        modified_indexed_nums = apply_modify_func(sorted_indexed_nums)

        result = [0] * len(nums)
        for index, new_value in modified_indexed_nums:
            result[index] = new_value

        return result

    clamp_error: int = 0

    def fix_value(min_value: int, max_value: int, value: int) -> Optional[int]:
        nonlocal clamp_error
        if clamp_error != 0 and not (min_value <= value <= max_value):
            if clamp_error > 0:
                clamp_error -= 1
                return value + 1
            else:
                clamp_error += 1
                return value - 1
        else:
            return None

    def distribute_points(weights: List[float], num_points: int, name: str) -> List[int]:
        weights_sum = sum(weights)
        logging.debug(f"\t{name}_{weights_sum=}")

        mean_1: List[float] = [stat / weights_sum for stat in weights]
        logging.debug(f"\t{name}_{mean_1=}")

        mean_rank: List[float] = [stat * num_points for stat in mean_1]
        logging.debug(f"\t{name}_{mean_rank=}")
        logging.debug(f"\t{name}_mean_rank_sum={sum(mean_rank)}")

        mean_rounded: List[int] = [round(stat) for stat in mean_rank]
        logging.debug(f"\t{name}_{mean_rounded=}")

        mean_clamped: List[int] = list()
        nonlocal clamp_error
        clamp_error = 0
        for stat in mean_rounded:
            clamped = clamp(stat, 2, 8)
            clamp_error += (stat - clamped)
            mean_clamped.append(clamped)
        logging.debug(f"\t{name}_{mean_clamped=}")
        logging.debug(f"\t{name}_{clamp_error=}")

        mean_clamped_fixed = sort_and_modify(mean_clamped, functools.partial(fix_value, 2, 8))
        logging.debug(f"\t{name}_{mean_clamped_fixed=}")

        return mean_clamped_fixed

    logging.debug("\nGenerating stats...")
    with open("Configs/stats.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        streetrat_table: List[List[int]] = data["streetrat_stats"][npc_template.role]
        columns: List[List[int]] = list(zip(*streetrat_table))

        stats_mean_line: List[float] = [sum(column) / len(column) for column in columns]
        logging.debug(f"\t{stats_mean_line=}")

        stats_mean_clamped_fixed = distribute_points(stats_mean_line,
                                                     npc_template.rank.stats_budget.generate(),
                                                     "stats")
        logging.debug(f"\t{stats_mean_clamped_fixed=}")

        stats_sum: int = 0
        for i, stat in enumerate(stats_mean_clamped_fixed):
            npc.stats[stat_type_from_int(i)] = stat
            stats_sum += stat

        logging.debug(f"\t{stats_sum=}")
        logging.debug(f"\t{npc_template.rank.stats_budget.mean=}")
        logging.debug(f"\t{npc_template.rank.stats_budget.standard_deviation=}")

    logging.debug("\nGenerating skills...")
    with open("Configs/skills.json", "r", encoding="utf-8") as f:
        def get_multiline_list(input_list, list_name) -> str:
            retval: str = ""
            retval += f"\t{list_name}=[\n"
            for elem in input_list:
                retval += f"\t\t{elem},\n"
            retval += f"\t]"
            return retval

        data = json.load(f)

        role_streetrat_skills_86 = data["streetrat_skills"][npc_template.role]
        logging.debug(get_multiline_list(role_streetrat_skills_86, "role_streetrat_skills_86"))

        role_streetrat_skills_1 = role_streetrat_skills_86
        for skill in role_streetrat_skills_1:
            skill["lvl"] /= 86
        logging.debug(get_multiline_list(role_streetrat_skills_1, "role_streetrat_skills_1"))

        role_streetrat_skills_rank = role_streetrat_skills_1
        role_skills_sum: int = 0
        for skill in role_streetrat_skills_rank:
            skill["lvl"] *= npc_template.rank.skills_budget.generate()
            role_skills_sum += skill["lvl"]
        logging.debug(get_multiline_list(role_streetrat_skills_rank, "role_streetrat_skills_rank"))

        role_streetrat_skills_rounded = role_streetrat_skills_rank
        rounded_skills_sum: int = 0
        for skill in role_streetrat_skills_rounded:
            skill["lvl"] = round(skill["lvl"])
            rounded_skills_sum += skill["lvl"]
        logging.debug(get_multiline_list(role_streetrat_skills_rounded, "role_streetrat_skills_rounded"))

        logging.debug(f"\t{rounded_skills_sum=}")
        logging.debug(f"\t{npc_template.rank.skills_budget.mean=}")
        logging.debug(f"\t{npc_template.rank.skills_budget.standard_deviation=}")

        for skill_pair in role_streetrat_skills_rounded:
            skill_name = skill_pair["skill"]
            skill_info = data["skills"][skill_name]
            skill = Skill(skill_name, StatType(skill_info["link"].lower()), SkillType(skill_info["type"]))
            npc.skills[skill] = skill_pair["lvl"]

    return npc
