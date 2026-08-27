#!/usr/bin/env python3
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/decision.schema.json").read_text())


def valid_decision(value):
    if not isinstance(value, dict):
        return False
    required = set(SCHEMA["required"])
    if set(value) != required:
        return False
    properties = SCHEMA["properties"]
    if value["decision"] not in properties["decision"]["enum"]:
        return False
    if value["reason_code"] not in properties["reason_code"]["enum"]:
        return False
    if value["source"] not in properties["source"]["enum"]:
        return False
    confidence = value["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return False
    if not 0 <= confidence <= 1:
        return False
    summary = value["summary"]
    if not isinstance(summary, str) or not 1 <= len(summary) <= 240:
        return False
    decision = value["decision"]
    reason = value["reason_code"]
    source = value["source"]
    if decision == "allow":
        return reason == "none" and source == "none"
    if decision == "clarify":
        return reason == "ambiguous_boundary" and source != "none"
    return reason not in {"none", "ambiguous_boundary"} and source != "none"


class ContractTests(unittest.TestCase):
    def test_checker_output_fixtures(self):
        fixtures = json.loads((ROOT / "tests/fixtures/checker_outputs.json").read_text())
        for fixture in fixtures:
            with self.subTest(fixture["id"]):
                self.assertEqual(valid_decision(fixture["output"]), fixture["valid"])

    def test_behavior_fixtures_are_replayable(self):
        fixtures = json.loads((ROOT / "tests/fixtures/checker_cases.json").read_text())
        categories = {fixture["category"] for fixture in fixtures}
        self.assertTrue({"benign", "benign_quote", "direct_injection", "indirect_injection",
                         "encoded_injection", "multilingual_injection", "multi_turn",
                         "ambiguous"}.issubset(categories))
        for fixture in fixtures:
            with self.subTest(fixture["id"]):
                self.assertTrue(fixture["policy_context"].strip())
                self.assertTrue(fixture["input"]["messages"])
                self.assertTrue(valid_decision(fixture["expected"]))

    def test_checker_prompt_names_contract(self):
        prompt = (ROOT / "checker/ACIP_Checker_v_1.0.md").read_text()
        self.assertIn("schemas/decision.schema.json", prompt)
        self.assertIn("not an authorization decision", prompt.replace("\n", " "))

    def test_consumer_docs_have_no_moving_network_installer(self):
        paths = [ROOT / "README.md", *sorted((ROOT / "integrations").rglob("*"))]
        text = "\n".join(path.read_text() for path in paths if path.is_file())
        self.assertNotIn("curl | bash", text)
        self.assertNotIn("raw.githubusercontent.com/Dicklesworthstone/acip/main", text)
        self.assertNotIn("api.github.com/repos/Dicklesworthstone/acip", text)


if __name__ == "__main__":
    unittest.main()
