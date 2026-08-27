#!/usr/bin/env python3
"""Replay committed checker outputs through the deterministic contract gate.

This validates evaluation data and expected structured decisions. It does not
execute or claim to measure a language model.
"""

import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from test_contract import valid_decision  # noqa: E402


fixtures = json.loads((ROOT / "tests/fixtures/checker_cases.json").read_text())
failures = []
for fixture in fixtures:
    expected = fixture.get("expected")
    if not fixture.get("policy_context") or not fixture.get("input", {}).get("messages"):
        failures.append(f"{fixture.get('id', '<unknown>')}: missing replay input")
    elif not valid_decision(expected):
        failures.append(f"{fixture['id']}: invalid expected decision")

if failures:
    print("\n".join(failures), file=sys.stderr)
    raise SystemExit(1)
print(f"replayed {len(fixtures)} deterministic checker fixtures")
