"""Check deployable character assets, integrity metadata and cup references."""

import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/foodball-go-site/"
REQUIRED_ASSETS = {"idle", "run_1", "run_2", "jump", "selection_default", "selection_player", "selection_cpu"}


def validate_asset(asset):
    url = urlparse(asset["url"])
    assert url.scheme == "https" and url.netloc == "ferfranky.github.io", asset["url"]
    assert url.path.startswith(PREFIX), asset["url"]
    path = (ROOT / unquote(url.path[len(PREFIX):])).resolve()
    assert path.is_relative_to(ROOT), path
    payload = path.read_bytes()
    assert 0 < len(payload) <= 8 * 1024 * 1024, path
    assert len(payload) == asset["bytes"], f"Wrong byte count: {path}"
    assert hashlib.sha256(payload).hexdigest() == asset["sha256"], f"Wrong hash: {path}"
    return len(payload)


def main():
    catalog = json.loads((ROOT / "live-content/catalog.json").read_text(encoding="utf-8"))
    assert catalog["schema_version"] == 1 and catalog["revision"]
    ids = set(catalog.get("character_overrides", {}))
    total = 0
    for character in catalog["characters"]:
        identifier = character["id"]
        assert identifier not in ids, f"Duplicate character: {identifier}"
        ids.add(identifier)
        assert REQUIRED_ASSETS == set(character["assets"]), identifier
        assert character["album_cards"], f"Client requires an album card: {identifier}"
        for locale in ("es", "en"):
            assert character["name"][locale], identifier
            for field in ("title", "role", "trait", "nationality", "bio"):
                assert 0 < len(character["story"][locale][field]) <= 280, (identifier, field)
        for asset in character["assets"].values():
            total += validate_asset(asset)
        for card in character["album_cards"]:
            validate_asset(card["asset"])
    for cup in catalog["tournaments"]:
        participants = cup["participants"]
        assert len(participants) == len(set(participants)), cup["id"]
        assert set(participants) <= ids, cup["id"]
        assert len(participants) >= cup["min_participants"], f"Insufficient cup roster: {cup['id']}"
        validate_asset(cup["art"])
    assert total <= 32 * 1024 * 1024, "Gameplay/selection assets exceed client sync budget"
    print(f"Character catalog valid: {len(catalog['characters'])} remote characters; {total:,} sync bytes")


if __name__ == "__main__":
    main()
