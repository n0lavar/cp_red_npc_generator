#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import dataclass_wizard
import json
import logging
import sys

from generate_trauma_team_status import generate_trauma_team_status
from generate_description import choose_nationality, generate_description
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
from logger import setup_logging
from args import create_and_parse_args
from utils import args_to_str, setup_random


def create_npc(npc_template: NpcTemplate,
               model_id: str,
               model_api_key: str,
               model_base_url: str,
               model_language: str,
               seed: int) -> Npc:
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
    npc = generate_description(npc, npc_template, model_id, model_api_key,
                               model_base_url, model_language, seed)
    return npc


def main() -> int:
    ranks = Rank.load()
    roles = Role.load()
    args: argparse.Namespace = create_and_parse_args(ranks, roles)

    setup_logging(args)
    seed: int = setup_random(args)

    args.nationality = args.nationality or choose_nationality()

    if args.rank.isnumeric():
        rank_number = int(args.rank)
        rank_json = ranks[rank_number]
    else:
        rank_number, rank_json = next((index, rank) for index, rank in enumerate(ranks) if rank["name"] == args.rank)

    rank: Rank = dataclass_wizard.fromdict(Rank, rank_json)
    rank.rank_number = rank_number
    role: Role = dataclass_wizard.fromdict(Role, next(r for r in roles if r["name"] == args.role))
    generation_rules: GenerationRules = dataclass_wizard.fromdict(GenerationRules, vars(args))

    # generation process, there are a lot of log lines with DEBUG level
    npc: Npc = create_npc(NpcTemplate(rank, role, generation_rules, args.nationality),
                          args.model_id,
                          args.model_api_key,
                          args.model_base_url,
                          args.model_language,
                          seed)

    if not args.foundry_json:
        # usually you have multiple npcs in one file and it's convenient to split them visually
        logging.info(
            f"<=================================================================================================>")

        # print the args you can use to receive exactly the same result
        args_dict = dict(vars(args))
        for key, value in args_dict.copy().items():
            args_dict[key.replace("_", "-")] = args_dict.pop(key)
        args_dict["seed"] = seed
        logging.info(f"\n{args_to_str(args_dict)}")

        # the long string with npc info
        npc_str: str = npc.to_string(args.flat)
        logging.info(npc_str)
    else:
        print(json.dumps(npc.to_dict_foundry_vvt(), ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
