from __future__ import annotations

import copy
import json
import sys
import unittest
from collections import Counter
from datetime import datetime, timedelta, timezone
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

    def test_christmas_cadences_and_rewards_preserve_existing_contract(self) -> None:
        season = next(s for s in self.liveops["seasons"] if s["id"] == "navidad_2026")
        previous = next(s for s in self.liveops["seasons"] if s["id"] == "dia_de_muertos_2026")
        self.assertEqual(season["status"], "published", "Future dates gate activation; scheduled never auto-activates in client")
        self.assertEqual(Counter(c["cadence"] for c in season["challenges"]), {"daily": 3, "weekly": 2, "season": 5})
        for current, old in zip(season["challenges"], previous["challenges"], strict=True):
            self.assertEqual(current["reward"], old["reward"])
            self.assertEqual(current["objective"]["event"], old["objective"]["event"])
            self.assertEqual(current["objective"]["target"], old["objective"]["target"])
            self.assertEqual(current["starts_at"], season["starts_at"])
            self.assertEqual(current["ends_at"], season["ends_at"])
        ponchito = next(c for c in season["challenges"] if c["id"] == "navidad_ponchito_15_goles")
        self.assertEqual(ponchito["objective"]["filters"]["player_character_ids"], ["ponche_navideno"])

    def test_christmas_dates_cover_full_mexico_city_days(self) -> None:
        season = next(s for s in self.liveops["seasons"] if s["id"] == "navidad_2026")
        start = datetime.fromisoformat(season["starts_at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(season["ends_at"].replace("Z", "+00:00"))
        mexico_city = timezone(timedelta(hours=-6))
        self.assertEqual(start.astimezone(mexico_city).isoformat(), "2026-12-01T00:00:00-06:00")
        self.assertEqual(end.astimezone(mexico_city).isoformat(), "2027-01-07T00:00:00-06:00")
        for timestamp, active in [
            ("2026-11-30T23:59:59-06:00", False),
            ("2026-12-01T00:00:00-06:00", True),
            ("2027-01-06T23:59:59-06:00", True),
            ("2027-01-07T00:00:00-06:00", False),
        ]:
            with self.subTest(timestamp=timestamp):
                self.assertEqual(start <= datetime.fromisoformat(timestamp) < end, active)

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
