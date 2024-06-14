#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import dataclass_wizard
import logging
import time
import sys
import numpy as np

from generate_ammo import generate_ammo
from generate_armor import generate_armor
from generate_cyberware import generate_cyberware
from generate_drugs import generate_drugs
from generate_equipment import generate_equipment
from generate_junk import generate_junk
from generate_stats import generate_stats_and_skills
from generate_weapon import generate_weapon
from npc import Npc
from npc_template import NpcTemplate, Rank, Role


def create_npc(npc_template: NpcTemplate) -> Npc:
    logging.debug(f"Input:")
    logging.debug(f"\trank: {npc_template.rank.name}")
    logging.debug(f"\trole: {npc_template.role.name}")

    npc = Npc()
    npc = generate_stats_and_skills(npc, npc_template)
    npc = generate_cyberware(npc, npc_template)
    npc = generate_weapon(npc, npc_template)
    npc = generate_ammo(npc, npc_template)
    npc = generate_equipment(npc, npc_template)
    npc = generate_armor(npc, npc_template)
    npc = generate_drugs(npc, npc_template)
    npc = generate_junk(npc, npc_template)
    return npc


def main(args) -> int:
    logging.basicConfig(level=logging.getLevelName(args.log_level), format="%(message)s")

    seed: int = 0
    if args.seed != 0:
        seed = args.seed
    else:
        seed = int(time.time_ns() % 1e9)
    np.random.seed(seed)

    rank: Rank = dataclass_wizard.fromdict(Rank, next(r for r in ranks if r["name"] == args.rank))
    role: Role = dataclass_wizard.fromdict(Role, next(r for r in roles if r["name"] == args.role))
    npc: Npc = create_npc(NpcTemplate(rank, role))
    npc_str: str = npc.to_string(args.flat)

    logging.info(f"\n{str(args.role).title()}, {str(args.rank).title()}, {seed=}")
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
                        choices=[r["name"] for r in ranks],
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
    parser.add_argument("--log_level",
                        type=str,
                        help="Logging level. Default is INFO.",
                        choices=list(logging.getLevelNamesMapping()),
                        default=logging.getLevelName(logging.INFO))

    return_code = main(parser.parse_args())
    sys.exit(return_code)
