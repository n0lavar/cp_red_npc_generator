#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import argparse

import dataclass_wizard
import logging

import equipment
import stats
from data import *


def create_npc(npc_template: NpcTemplate) -> Npc:
    logging.debug(f"Input:")
    logging.debug(f"\trank: {npc_template.rank.name}")
    logging.debug(f"\trole: {npc_template.role}")
    logging.debug(f"\tgang: {npc_template.gang}")

    npc = Npc()
    npc = stats.create_stats(npc, npc_template)
    npc = equipment.create_equipment(npc, npc_template)
    return npc


def get_ranks():
    with open("Configs/ranks.json", "r", encoding="utf-8") as f:
        return json.load(f)


def main(args) -> int:
    logging.basicConfig(level=logging.getLevelName(args.log_level), format="%(message)s")
    rank_data = dataclass_wizard.fromdict(Rank, next(r for r in ranks if r["name"] == args.rank))
    npc = create_npc(NpcTemplate(rank_data, args.gang, args.role))
    logging.info(f"{npc}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    ranks = get_ranks()
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
                        type=RoleType,
                        help="An occupation the NPC is known by on The Street. "
                             "`civilian` means that this is just a regular human, "
                             "`booster` means that this is a street mook with some fighting skills,"
                             " but without any specialization. "
                             "The role can determine the equipment and the direction of the NPC's skills. "
                             "The default value is `booster`. ",
                        choices=list(RoleType),
                        default=RoleType.BOOSTER)
    parser.add_argument("--gang",
                        type=GangType,
                        help="The affiliation of this NPC. "
                             "It can determine equipment preferences. "
                             "The default value is `boosters`.",
                        choices=list(GangType),
                        default=GangType.BOOSTERS)
    parser.add_argument("--log_level",
                        type=str,
                        help="Logging level. Default is INFO.",
                        choices=list(logging.getLevelNamesMapping()),
                        default=logging.getLevelName(logging.INFO))

    return_code = main(parser.parse_args())
    exit(return_code)
