#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import dataclass_wizard
import json
import logging
import sys

from pathlib import Path

from generate_trauma_team_status import generate_trauma_team_status
from generate_description import NATIONALITIES, choose_nationality, generate_description
from logger import setup_logging
from utils import args_to_str, get_default_value, setup_random
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


def find_settings_path() -> Path:
    candidates = [Path.cwd() / "settings.json"]
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent / "settings.json")
    else:
        candidates.append(Path(__file__).resolve().parents[2] / "settings.json")

    for settings_path in candidates:
        if settings_path.is_file():
            return settings_path

    return candidates[0]


def load_settings() -> dict:
    settings_path = find_settings_path()
    if not settings_path.is_file():
        return {}

    with settings_path.open(encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    if not isinstance(settings, dict):
        raise ValueError(f"{settings_path} must contain a JSON object")

    return {key.replace("-", "_"): value for key, value in settings.items()}


def create_and_parse_args(ranks, roles) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    npc_customization_group = parser.add_argument_group("NPC Customization")
    npc_customization_group.add_argument("--rank",
                                         type=str,
                                         help="A measure of the development of a given NPC, "
                                              "where private is an unskilled and unknown newcomer, "
                                              "and general is a world-class character. "
                                              "Rank determines how advanced an NPC's skills are and "
                                              "how cool his equipment is.",
                                         choices=[r["name"] for r in ranks] + [str(i) for i in range(len(ranks))],
                                         default="captain")
    npc_customization_group.add_argument("--role",
                                         type=str,
                                         help="An occupation the NPC is known by on The Street. "
                                              "`civilian` means that this is just a regular human. "
                                              "The role can determine the equipment and the direction of the NPC's skills. "
                                              "The default value is `solo`. ",
                                         choices=[r["name"] for r in roles],
                                         default="solo")
    npc_customization_group.add_argument("--nationality",
                                         type=str,
                                         help="Faker locale used to generate the NPC name, e.g. ru_RU or en_US. "
                                              "If omitted, a random nationality is used.",
                                         choices=NATIONALITIES,
                                         default=None)
    npc_customization_group.add_argument("--allow-non-basic-ammo",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow non-basic ammo, such as armor piercing and expansive.",
                                         default=get_default_value(GenerationRules, "allow-non-basic-ammo"))
    npc_customization_group.add_argument("--allow-grenades",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow grenades",
                                         default=get_default_value(GenerationRules, "allow-grenades"))
    npc_customization_group.add_argument("--allow-armor",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow armor items (cyberware armor will still be there).",
                                         default=get_default_value(GenerationRules, "allow-armor"))
    npc_customization_group.add_argument("--allow-cyberware",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow cyberware.",
                                         default=get_default_value(GenerationRules, "allow-cyberware"))
    npc_customization_group.add_argument("--allow-borgware",
                                         action=argparse.BooleanOptionalAction,
                                         help="If specified, allow borgware. "
                                              "Usually you don't want the regular mooks to use that cool stuff.",
                                         default=get_default_value(GenerationRules, "allow-borgware"))
    npc_customization_group.add_argument("--allow-drugs",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow adding drugs. "
                                              "Drugs may be added or not depending on airhypo generation.",
                                         default=get_default_value(GenerationRules, "allow-drugs"))
    npc_customization_group.add_argument("--allow-equipment",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow equipment, such as flashlight and airhypo "
                                              "(cyberware equipment will still be there). ",
                                         default=get_default_value(GenerationRules, "allow-equipment"))
    npc_customization_group.add_argument("--allow-money",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow money.",
                                         default=get_default_value(GenerationRules, "allow-money"))
    npc_customization_group.add_argument("--allow-junk",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow useless junk for flavor. ",
                                         default=get_default_value(GenerationRules, "allow-junk"))
    npc_customization_group.add_argument("--allow-melee-weapon",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow melee weapon "
                                              "(brawling, martial arts and cyberware weapons will still be there).",
                                         default=get_default_value(GenerationRules, "allow-melee-weapon"))
    npc_customization_group.add_argument("--allow-ranged-weapon",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow ranged weapon (cyberware weapons will still be there).",
                                         default=get_default_value(GenerationRules, "allow-ranged-weapon"))
    npc_customization_group.add_argument("--allow-martial-arts",
                                         action=argparse.BooleanOptionalAction,
                                         help="Is specified, allow martial arts (brawling will still be there).",
                                         default=get_default_value(GenerationRules, "allow-martial-arts"))

    generation_settings_group = parser.add_argument_group("Generation settings")
    generation_settings_group.add_argument("--seed",
                                           type=int,
                                           help="A number for a random engine. The same seed will always give the same result when "
                                                "the other arguments are unchanged. The default is 0, which means \"use unix epoch\".",
                                           default=0)
    generation_settings_group.add_argument("--model-id",
                                           type=str,
                                           help="Model identifier used to generate the NPC description.",
                                           default="qwen/qwen3.6-35b-a3b")
    generation_settings_group.add_argument("--model-api-key",
                                           type=str,
                                           help="API key for the OpenAI-compatible model server.",
                                           default="lm-studio")
    generation_settings_group.add_argument("--model-base-url",
                                           type=str,
                                           help="Base URL of the OpenAI-compatible model server.",
                                           default="http://localhost:1234/v1")
    generation_settings_group.add_argument("--model-language",
                                           type=str,
                                           help="Language in which the model generates the NPC description.",
                                           default="English")

    appearance_group = parser.add_argument_group("Appearance")
    appearance_group.add_argument("--flat",
                                  action=argparse.BooleanOptionalAction,
                                  help="If specified, don't use columns. "
                                       "Easier for editing and copy-pasting, but takes much more space.")
    appearance_group.add_argument("--foundry-json",
                                  action=argparse.BooleanOptionalAction,
                                  help="If specified, output results in JSON format that is suitable for Foundry VVT.",
                                  default=False)
    appearance_group.add_argument("--log-level",
                                  type=str,
                                  help="Logging level. Default is INFO.",
                                  choices=list(logging.getLevelNamesMapping()),
                                  default=logging.getLevelName(logging.INFO))

    known_arguments = {action.dest for action in parser._actions}
    settings = load_settings()
    unknown_settings = settings.keys() - known_arguments
    if unknown_settings:
        parser.error(f"unknown settings: {', '.join(sorted(unknown_settings))}")
    parser.set_defaults(**settings)

    return parser.parse_args()


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
