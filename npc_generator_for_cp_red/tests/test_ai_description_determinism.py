import json
import sys
from unittest.mock import Mock, patch

from base_test import BaseTest, PROJECT_DIR

sys.path.insert(0, str(PROJECT_DIR.parent))
sys.path.insert(0, str(PROJECT_DIR / "src"))
from generate_description import _generate_ai_description
from item import Item, ItemType
from npc import Npc
from npc_template import GenerationRules, NpcTemplate, Rank, Role


class AiDescriptionDeterminismTest(BaseTest):
    def test_same_seed_and_semantic_npc_produce_same_request_payload(self):
        template = NpcTemplate(Rank(), Role("solo"), GenerationRules(), "en_US")
        payloads = []

        response = Mock()
        response.read.return_value = b'{"choices":[{"message":{"content":"Description"}}]}'
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)

        def capture_payload(http_request, timeout):
            payloads.append(json.loads(http_request.data.decode("utf-8")))
            return response

        with patch("generate_description.request.urlopen", side_effect=capture_payload):
            for _ in range(2):
                npc = Npc()
                npc.weapons.add(Item(name="Test weapon", type=ItemType.WEAPON,
                                     damage="2d6", rate_of_fire=2))
                _generate_ai_description(
                    npc, template, "model", "api-key", "http://model/v1", "English", 123456)

        self.assertEqual(payloads[0], payloads[1])