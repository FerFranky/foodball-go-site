"""Check deployable character assets, integrity metadata and cup references."""

import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/foodball-go-site/"
REQUIRED_ASSETS = {"idle", "run_1", "run_2", "jump", "selection_default", "selection_player", "selection_cpu"}
SELECTION_KEYS = {"default", "player", "cpu"}


def webp_dimensions(payload):
    assert payload[:4] == b"RIFF" and payload[8:12] == b"WEBP", "Expected WebP image"
    offset = 12
    while offset + 8 <= len(payload):
        kind = payload[offset:offset + 4]
        length = int.from_bytes(payload[offset + 4:offset + 8], "little")
        data = payload[offset + 8:offset + 8 + length]
        assert len(data) == length, "Truncated WebP chunk"
        if kind == b"VP8X":
            return 1 + int.from_bytes(data[4:7], "little"), 1 + int.from_bytes(data[7:10], "little")
        if kind == b"VP8 ":
            assert data[3:6] == b"\x9d\x01\x2a", "Invalid VP8 frame"
            return int.from_bytes(data[6:8], "little") & 0x3fff, int.from_bytes(data[8:10], "little") & 0x3fff
        if kind == b"VP8L":
            assert data[0] == 0x2f, "Invalid VP8L frame"
            bits = int.from_bytes(data[1:5], "little")
            return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
        offset += 8 + length + (length % 2)
    raise AssertionError("Missing WebP image dimensions")


def validate_asset(asset, dimensions=None):
    url = urlparse(asset["url"])
    assert url.scheme == "https" and url.netloc == "ferfranky.github.io", asset["url"]
    assert url.path.startswith(PREFIX), asset["url"]
    path = (ROOT / unquote(url.path[len(PREFIX):])).resolve()
    assert path.is_relative_to(ROOT), path
    payload = path.read_bytes()
    assert 0 < len(payload) <= 8 * 1024 * 1024, path
    assert len(payload) == asset["bytes"], f"Wrong byte count: {path}"
    assert hashlib.sha256(payload).hexdigest() == asset["sha256"], f"Wrong hash: {path}"
    if dimensions is not None:
        assert webp_dimensions(payload) == dimensions, f"Wrong selection dimensions: {path}"
    return len(payload)


def validate_selection_assets(assets):
    assert isinstance(assets, dict) and set(assets) == SELECTION_KEYS, "Selection art requires default/player/cpu"
    return sum(validate_asset(asset, (512, 512)) for asset in assets.values())


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
    for override in catalog.get("character_overrides", {}).values():
        if "selection_assets" in override:
            total += validate_selection_assets(override["selection_assets"])
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
