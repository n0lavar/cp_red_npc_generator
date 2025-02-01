#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import logging
import math
import numpy as np
from typing import List, Optional, Callable

from npc import Npc
from npc_template import NpcTemplate
from stats import Skill, StatType, SkillType
from utils import clamp, load_data


def generate_stats_and_skills(npc: Npc, npc_template: NpcTemplate) -> Npc:
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

    def distribute_points(weights: List[float],
                          num_points: float,
                          min_value: int,
                          max_value: int,
                          name: str) -> List[int]:
        nonlocal clamp_error

        logging.debug(f"\t{name}_{weights=}")
        logging.debug(f"\t{name}_{num_points=}")
        logging.debug(f"\t{name}_{min_value=}")
        logging.debug(f"\t{name}_{max_value=}")

        weights_sum = sum(weights)
        logging.debug(f"\t{name}_{weights_sum=}")

        mean_1: List[float] = [weight / weights_sum for weight in weights]
        logging.debug(f"\t{name}_{mean_1=}")

        mean_rank: List[float] = [mean * num_points for mean in mean_1]
        logging.debug(f"\t{name}_{mean_rank=}")

        mean_rounded: List[int] = [round(mean) for mean in mean_rank]
        logging.debug(f"\t{name}_{mean_rounded=}")

        mean_clamped: List[int] = list()
        clamp_error = 0
        for mean in mean_rounded:
            clamped = clamp(mean, 2, 8)
            clamp_error += (mean - clamped)
            mean_clamped.append(clamped)
        logging.debug(f"\t{name}_{mean_clamped=}")
        logging.debug(f"\t{name}_{clamp_error=}")

        mean_clamped_fixed = sort_and_modify(mean_clamped, functools.partial(fix_value, min_value, max_value))
        logging.debug(f"\t{name}_{mean_clamped_fixed=}")

        return mean_clamped_fixed

    logging.debug("\nGenerating stats...")
    stats_data = load_data("configs/stats.json")

    streetrat_stats_table: List[List[int]] = stats_data["streetrat_stats"][npc_template.role.name]
    streetrat_chosen_table: List[int] = streetrat_stats_table[np.random.choice(len(streetrat_stats_table))]
    stats_mean_clamped_distributed = distribute_points(
        streetrat_chosen_table,
        npc_template.rank.stats_budget.generate(),
        2,
        8,
        "stats")

    stats_sum: int = 0
    for i, stat in enumerate(stats_mean_clamped_distributed):
        npc.stats[StatType(i + 1)] = stat
        stats_sum += stat

    logging.debug(f"\t{stats_sum=}")
    logging.debug(f"\t{npc_template.rank.stats_budget.mean=}")
    logging.debug(f"\t{npc_template.rank.stats_budget.standard_deviation=}")

    logging.debug("\nGenerating skills...")
    skills_data = load_data("configs/skills.json")

    # add all skills with level 0
    for skill_name, skill_info in skills_data.items():
        skill = Skill(skill_name, StatType[skill_info["link"]], SkillType(skill_info["type"]))
        npc.skills.setdefault(skill, 0)

    # increase values for role-specific skills
    role_streetrat_skills_line: List[int] = [skill_level for _, skill_level in npc_template.role.skills.items()]
    role_streetrat_skills_distributed = distribute_points(
        role_streetrat_skills_line,
        npc_template.rank.skills_budget.generate(),
        2,
        10,
        "skills")

    skills_sum: int = 0
    for i, skill_name in enumerate(npc_template.role.skills):
        skill_info = skills_data[skill_name]
        skill = Skill(skill_name, StatType[skill_info["link"]], SkillType(skill_info["type"]))
        npc.skills[skill] += role_streetrat_skills_distributed[i]
        skills_sum += role_streetrat_skills_distributed[i]

    # possibly replace Brawling with MartialArts
    if (npc_template.generation_rules.allow_martial_arts
            and np.random.uniform(0, 1) < npc_template.role.martial_arts_probability):
        brawling_skill = next(s for s in npc.skills.keys() if s.name == "Brawling")
        brawling_skill_value = npc.skills[brawling_skill]

        martial_arts_skill = next(s for s in npc.skills.keys() if s.name == "MartialArts")
        # brawling can't be less than 2
        new_martial_arts_skill_value = math.ceil((brawling_skill_value - 2) / 2)

        if new_martial_arts_skill_value > 0:
            npc.skills[brawling_skill] = 2
            npc.skills[martial_arts_skill] = new_martial_arts_skill_value

    logging.debug(f"\t{skills_sum=}")
    logging.debug(f"\t{npc_template.rank.skills_budget.mean=}")
    logging.debug(f"\t{npc_template.rank.skills_budget.standard_deviation=}")

    return npc
