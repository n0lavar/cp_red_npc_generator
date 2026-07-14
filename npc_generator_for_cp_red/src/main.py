#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import dataclass_wizard
import logging
import time
import sys
import numpy as np

from generate_trauma_team_status import generate_trauma_team_status
from utils import is_debugger_active, args_to_str, get_default_value
from generate_ammo import generate_ammo
from generate_armor import generate_armor
from generate_cyberware import generate_cyberware
from generate_drugs import generate_drugs
from generate_equipment import generate_equipment
from generate_junk import generate_junk
from generate_stats import generate_stats_and_skills
from generate_weapon import generate_weapon
from npc import Npc
from npc_template import NpcTemplate, Rank, Role, GenerationRules


def create_npc(npc_template: NpcTemplate) -> Npc:
    logging.debug(f"Input:")
    logging.debug(f"\trank: {npc_template.rank.name}")
    logging.debug(f"\trole: {npc_template.role.name}")
    logging.debug(f"\tgeneration_rules: {npc_template.generation_rules}")

    npc = Npc()
    npc = generate_stats_and_skills(npc, npc_template)
    npc = generate_cyberware(npc, npc_template)
    npc = generate_weapon(npc, npc_template)
    npc = generate_ammo(npc, npc_template)
    npc = generate_equipment(npc, npc_template)
    npc = generate_armor(npc, npc_template)
    npc = generate_drugs(npc, npc_template)
    npc = generate_junk(npc, npc_template)
    npc = generate_trauma_team_status(npc, npc_template)
    return npc


def main(args) -> int:
    logging.basicConfig(level=logging.DEBUG if is_debugger_active() else logging.getLevelName(args.log_level),
                        format="%(message)s")

    seed: int = 0
    if args.seed != 0:
        seed = args.seed
    else:
        seed = int(time.time_ns() % 1e9)
    np.random.seed(seed)

    if args.rank.isnumeric():
        rank_json = ranks[int(args.rank)]
    else:
        rank_json = next(r for r in ranks if r["name"] == args.rank)

    rank: Rank = dataclass_wizard.fromdict(Rank, rank_json)
    role: Role = dataclass_wizard.fromdict(Role, next(r for r in roles if r["name"] == args.role))
    generation_rules: GenerationRules = dataclass_wizard.fromdict(GenerationRules, vars(args))

    # generation process, there are a lot of log lines with DEBUG level
    npc: Npc = create_npc(NpcTemplate(rank, role, generation_rules))
    npc_str: str = npc.to_string(args.flat)

    # usually you have multiple npcs in one file and it's convenient to split them visually
    logging.info(f"<=================================================================================================>")

    # print the args you can use to receive exactly the same result
    args_dict = dict(vars(args))
    for key, value in args_dict.copy().items():
        args_dict[key.replace("_", "-")] = args_dict.pop(key)
    args_dict["seed"] = seed
    logging.info(f"\n{args_to_str(args_dict)}")

    # the long string with npc info
    logging.info(npc_str)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    ranks = Rank.load()
    roles = Role.load()
    parser.add_argument("--rank",
                        type=str,
                        help="A measure of the development of a given NPC, "
                             "where private is an unskilled and unknown newcomer, "
                             "and general is a world-class character. "
                             "Rank determines how advanced an NPC's skills are and "
                             "how cool his equipment is.",
                        choices=[r["name"] for r in ranks] + [str(i) for i in range(len(ranks))],
                        default="captain")
    parser.add_argument("--role",
                        type=str,
                        help="An occupation the NPC is known by on The Street. "
                             "`civilian` means that this is just a regular human. "
                             "The role can determine the equipment and the direction of the NPC's skills. "
                             "The default value is `solo`. ",
                        choices=[r["name"] for r in roles],
                        default="solo")
    parser.add_argument("--seed",
                        type=int,
                        help="A number for a random engine. The same seed will always give the same result when "
                             "the other arguments are unchanged. The default is 0, which means \"use unix epoch\".",
                        default=0)
    parser.add_argument("--flat",
                        action=argparse.BooleanOptionalAction,
                        help="If specified, don't use columns. "
                             "Easier for editing and copy-pasting, but takes much more space.")
    parser.add_argument("--log-level",
                        type=str,
                        help="Logging level. Default is INFO.",
                        choices=list(logging.getLevelNamesMapping()),
                        default=logging.getLevelName(logging.INFO))
    parser.add_argument("--allow-non-basic-ammo",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow non-basic ammo, such as armor piercing and expansive.",
                        default=get_default_value(GenerationRules, "allow-non-basic-ammo"))
    parser.add_argument("--allow-grenades",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow grenades",
                        default=get_default_value(GenerationRules, "allow-grenades"))
    parser.add_argument("--allow-armor",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow armor items (cyberware armor will still be there).",
                        default=get_default_value(GenerationRules, "allow-armor"))
    parser.add_argument("--allow-cyberware",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow cyberware.",
                        default=get_default_value(GenerationRules, "allow-cyberware"))
    parser.add_argument("--allow-borgware",
                        action=argparse.BooleanOptionalAction,
                        help="If specified, allow borgware. "
                             "Usually you don't want the regular mooks to use that cool stuff.",
                        default=get_default_value(GenerationRules, "allow-borgware"))
    parser.add_argument("--allow-drugs",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow adding drugs. "
                             "Drugs may be added or not depending on airhypo generation.",
                        default=get_default_value(GenerationRules, "allow-drugs"))
    parser.add_argument("--allow-equipment",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow equipment, such as flashlight and airhypo "
                             "(cyberware equipment will still be there). ",
                        default=get_default_value(GenerationRules, "allow-equipment"))
    parser.add_argument("--allow-money",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow money.",
                        default=get_default_value(GenerationRules, "allow-money"))
    parser.add_argument("--allow-junk",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow useless junk for flavor. ",
                        default=get_default_value(GenerationRules, "allow-junk"))
    parser.add_argument("--allow-melee-weapon",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow melee weapon "
                             "(brawling, martial arts and cyberware weapons will still be there).",
                        default=get_default_value(GenerationRules, "allow-melee-weapon"))
    parser.add_argument("--allow-ranged-weapon",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow ranged weapon (cyberware weapons will still be there).",
                        default=get_default_value(GenerationRules, "allow-ranged-weapon"))
    parser.add_argument("--allow-martial-arts",
                        action=argparse.BooleanOptionalAction,
                        help="Is specified, allow martial arts (brawling will still be there).",
                        default=get_default_value(GenerationRules, "allow-martial-arts"))

    return_code = main(parser.parse_args())
    sys.exit(return_code)
