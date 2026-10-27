"""Regression checks for the optional selection-art deployment contract."""

import copy
import json
import unittest

from scripts import validate_catalog as validator


class SelectionCatalogTests(unittest.TestCase):
    def setUp(self):
        catalog = json.loads((validator.ROOT / "live-content/catalog.json").read_text(encoding="utf-8"))
        self.assets = catalog["character_overrides"]["Burger"]["selection_assets"]

    def test_published_selection_package_has_real_square_assets(self):
        self.assertGreater(validator.validate_selection_assets(self.assets), 0)

    def test_partial_selection_package_is_rejected(self):
        with self.assertRaises(AssertionError):
            validator.validate_selection_assets({"default": self.assets["default"]})

    def test_integrity_mismatch_is_rejected(self):
        assets = copy.deepcopy(self.assets)
        assets["player"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(AssertionError, "Wrong hash"):
            validator.validate_selection_assets(assets)

    def test_selection_shape_is_enforced(self):
        with self.assertRaisesRegex(AssertionError, "Wrong selection dimensions"):
            validator.validate_asset(self.assets["default"], (512, 768))

    def test_pancho_has_complete_square_selection_states(self):
        catalog = json.loads((validator.ROOT / "live-content/catalog.json").read_text(encoding="utf-8"))
        pancho = next(entry for entry in catalog["characters"] if entry["id"] == "pan_de_muerto")
        for state in ("default", "player", "cpu"):
            self.assertGreater(validator.validate_asset(pancho["assets"][f"selection_{state}"], (512, 512)), 0)


if __name__ == "__main__":
    unittest.main()
