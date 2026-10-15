from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))
from validate_liveops import ValidationError, load_json, validate_liveops  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


class LiveOpsValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_json(ROOT / "live-content/catalog.json")
        self.liveops = load_json(ROOT / "live-content/liveops.json")

    def test_current_catalog_is_valid(self) -> None:
        validate_liveops(self.liveops, self.catalog)

    def test_duplicate_ids_are_rejected(self) -> None:
        invalid = copy.deepcopy(self.liveops)
        invalid["achievements"][0]["id"] = invalid["seasons"][0]["challenges"][0]["id"]
        with self.assertRaisesRegex(ValidationError, "duplicate id"):
            validate_liveops(invalid, self.catalog)

    def test_unknown_tournament_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.liveops)
        invalid["seasons"][0]["challenges"][3]["objective"]["filters"]["tournament_ids"] = ["missing_cup"]
        with self.assertRaisesRegex(ValidationError, "unknown id"):
            validate_liveops(invalid, self.catalog)

    def test_malformed_art_hash_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.liveops)
        invalid["seasons"][0]["art"] = {
            "url": "https://example.invalid/season.webp",
            "bytes": 1,
            "sha256": "not-a-hash",
        }
        with self.assertRaisesRegex(ValidationError, "SHA-256"):
            validate_liveops(invalid, self.catalog)


if __name__ == "__main__":
    unittest.main()
