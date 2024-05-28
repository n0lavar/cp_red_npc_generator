#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import dataclass_wizard
import logging

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
    logging.debug(f"\trole: {npc_template.role}")

    npc = Npc()
    npc = generate_stats_and_skills(npc, npc_template)
    npc = generate_cyberware(npc, npc_template)
    npc = generate_armor(npc, npc_template)
    npc = generate_weapon(npc, npc_template)
    npc = generate_ammo(npc, npc_template)
    npc = generate_equipment(npc, npc_template)
    npc = generate_drugs(npc, npc_template)
    npc = generate_junk(npc, npc_template)
    return npc


def main(args) -> int:
    logging.basicConfig(level=logging.getLevelName(args.log_level), format="%(message)s")
    rank_data = dataclass_wizard.fromdict(Rank, next(r for r in ranks if r["name"] == args.rank))
    role_data = dataclass_wizard.fromdict(Role, next(r for r in roles if r["name"] == args.role))
    npc = create_npc(NpcTemplate(rank_data, role_data))
    logging.info(f"{str(args.role).title()}, {str(args.rank).title()}")
    logging.info(f"{npc}")
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
                        required=True)
    parser.add_argument("--role",
                        type=str,
                        help="An occupation the NPC is known by on The Street. "
                             "`civilian` means that this is just a regular human, "
                             "`booster` means that this is a street mook with some fighting skills,"
                             " but without any specialization. "
                             "The role can determine the equipment and the direction of the NPC's skills. "
                             "The default value is `booster`. ",
                        choices=[r["name"] for r in roles],
                        default="booster")
    parser.add_argument("--log_level",
                        type=str,
                        help="Logging level. Default is INFO.",
                        choices=list(logging.getLevelNamesMapping()),
                        default=logging.getLevelName(logging.INFO))

    return_code = main(parser.parse_args())
    exit(return_code)
