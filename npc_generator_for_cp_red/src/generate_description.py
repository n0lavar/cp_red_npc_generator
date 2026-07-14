#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import numpy as np

from faker import Faker
from faker.config import AVAILABLE_LOCALES
from unidecode import unidecode

from npc import Npc
from npc_template import NpcTemplate
from utils import load_data

POPULATIONS = load_data("configs/nationality_weights.json")["populations"]
NATIONALITIES = sorted(
    locale for locale in AVAILABLE_LOCALES
    if locale.rsplit("_", 1)[-1] in POPULATIONS
)

_locales_per_country = Counter(locale.rsplit("_", 1)[-1] for locale in NATIONALITIES)
_nationality_weights = np.array([
    POPULATIONS[locale.rsplit("_", 1)[-1]] / _locales_per_country[locale.rsplit("_", 1)[-1]]
    for locale in NATIONALITIES
], dtype=float)
_probability_order = np.argsort(-_nationality_weights, kind="stable")
NATIONALITIES = [NATIONALITIES[index] for index in _probability_order]
_nationality_weights = _nationality_weights[_probability_order]
NATIONALITY_PROBABILITIES = _nationality_weights / _nationality_weights.sum()


def choose_nationality() -> str:
    return str(np.random.choice(NATIONALITIES, p=NATIONALITY_PROBABILITIES))


def generate_description(npc: Npc, npc_template: NpcTemplate) -> Npc:
    """Generate an ASCII-only NPC name for the requested nationality."""
    faker = Faker(npc_template.nationality)
    faker.seed_instance(int(np.random.randint(0, 2 ** 32, dtype=np.uint32)))
    npc.name = unidecode(faker.first_name())
    npc.surname = unidecode(faker.last_name())
    return npc
