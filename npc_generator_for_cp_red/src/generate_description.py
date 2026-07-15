#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
from collections.abc import Set
import json
import logging
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from urllib import error, request
import numpy as np

from faker import Faker
from faker.config import AVAILABLE_LOCALES
from unidecode import unidecode

from npc import Npc
from npc_template import NpcTemplate
from utils import load_data
from normal_distribution import NormalDistribution

_POPULATIONS = load_data("configs/nationality_weights.json")["populations"]
_DESCRIPTION_PROMPT = Path("configs/description_prompt.md").read_text(
    encoding="utf-8"
).strip()
NATIONALITIES = sorted(
    locale for locale in AVAILABLE_LOCALES
    if locale.rsplit("_", 1)[-1] in _POPULATIONS
)

_locales_per_country = Counter(locale.rsplit("_", 1)[-1] for locale in NATIONALITIES)
_nationality_weights = np.array([
    _POPULATIONS[locale.rsplit("_", 1)[-1]] / _locales_per_country[locale.rsplit("_", 1)[-1]]
    for locale in NATIONALITIES
], dtype=float)
_probability_order = np.argsort(-_nationality_weights, kind="stable")
NATIONALITIES = [NATIONALITIES[index] for index in _probability_order]
_nationality_weights = _nationality_weights[_probability_order]
NATIONALITY_PROBABILITIES = _nationality_weights / _nationality_weights.sum()
_VOLATILE_DATACLASS_FIELDS = {"id", "creation_time"}


def choose_nationality() -> str:
    return str(np.random.choice(NATIONALITIES, p=NATIONALITY_PROBABILITIES))


def _generate_name_surname(npc: Npc, npc_template: NpcTemplate) -> Npc:
    faker = Faker(npc_template.nationality)
    if npc.sex:
        npc.name = unidecode(faker.first_name_male())
        npc.surname = unidecode(faker.last_name_male())
    else:
        npc.name = unidecode(faker.first_name_female())
        npc.surname = unidecode(faker.last_name_female())

    return npc


def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.name
    if is_dataclass(value):
        return {
            item.name: _json_value(getattr(value, item.name))
            for item in fields(value)
            if item.name not in _VOLATILE_DATACLASS_FIELDS
        }
    if isinstance(value, dict):
        return {str(_json_value(key)): _json_value(item) for key, item in value.items()}
    if isinstance(value, Set):
        return [_json_value(item) for item in value]
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _generate_ai_description(npc: Npc,
                             npc_template: NpcTemplate,
                             model_id: Optional[str],
                             model_api_key: Optional[str],
                             model_base_url: Optional[str],
                             model_language: str,
                             seed: int) -> Npc:
    if not all((model_id, model_api_key, model_base_url)):
        return npc

    npc_data = _json_value(npc)
    npc_data.pop("description", None)
    context = {"npc": npc_data, "npc_template": _json_value(npc_template)}
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": f"{_DESCRIPTION_PROMPT} Write the description in {model_language}."
            },
            {
                "role": "user",
                "content": json.dumps(context, ensure_ascii=False)
            },
        ],
        "temperature": 0.5,
        "seed": seed,
    }
    http_request = request.Request(
        model_base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {model_api_key}", "Content-Type": "application/json"},
        method="POST")
    try:
        with request.urlopen(http_request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        description = result["choices"][0]["message"]["content"].strip()
        if description:
            npc.description = description
    except (error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        logging.warning("AI description was not generated: %s", exc)
    return npc


def generate_description(npc: Npc,
                         npc_template: NpcTemplate,
                         model_id: Optional[str],
                         model_api_key: Optional[str],
                         model_base_url: Optional[str],
                         model_language: str = "English",
                         seed: int = 0) -> Npc:
    npc.sex = np.random.choice([True, False])
    npc.nationality = npc_template.nationality
    npc.age = round(NormalDistribution(20 + 5 * npc_template.rank.rank_number, 2).generate())
    npc = _generate_name_surname(npc, npc_template)
    npc = _generate_ai_description(npc, npc_template, model_id, model_api_key,
                                   model_base_url, model_language, seed)
    return npc
