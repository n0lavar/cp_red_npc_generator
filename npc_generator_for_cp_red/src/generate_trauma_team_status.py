#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
import numpy as np

from npc import Npc
from npc_template import NpcTemplate, TraumaTeamStatusType


def generate_trauma_team_status(npc: Npc, npc_template: NpcTemplate) -> Npc:
    weights: List[float] = npc_template.rank.trauma_team_status_weights
    if len(weights) == 0:
        return npc

    assert len(weights) == len(TraumaTeamStatusType)
    assert all(x >= 0 for x in weights)

    probabilities: List[float] = [x / sum(weights) for x in weights]
    index: int = np.random.choice(len(weights), p=probabilities)
    npc.trauma_team_status = TraumaTeamStatusType(index + 1)
    return npc
