#!/usr/bin/env python3
"""Validate the static Foodball Go LiveOps catalog without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")
VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
EVENTS = {
    "goal_scored",
    "own_goal_scored",
    "match_won",
    "match_completed",
    "tournament_match_won",
    "tournament_completed",
    "tournament_won",
    "tournament_round_reached",
}
TOURNAMENT_EVENTS = {
    "tournament_match_won",
    "tournament_completed",
    "tournament_won",
    "tournament_round_reached",
}
GAME_MODES = {"free_play", "tournament"}
ROUNDS = {"quarterfinal", "semifinal", "final", "champion"}


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: root must be an object")
    return value


def expect_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must be an object")
    return value


def expect_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{path} must be an array")
    return value


def expect_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be a non-empty string")
    return value


def expect_positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValidationError(f"{path} must be a positive integer")
    return value


def validate_id(value: Any, path: str) -> str:
    identifier = expect_string(value, path)
    if not ID_PATTERN.fullmatch(identifier):
        raise ValidationError(f"{path} must match {ID_PATTERN.pattern}")
    return identifier


def parse_utc(value: Any, path: str) -> datetime:
    timestamp = expect_string(value, path)
    if not timestamp.endswith("Z"):
        raise ValidationError(f"{path} must be an ISO-8601 UTC timestamp ending in Z")
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{path} is not a valid ISO-8601 timestamp") from exc


def reject_unknown_keys(value: dict[str, Any], allowed: set[str], path: str) -> None:
    unknown = set(value) - allowed
    if unknown:
        raise ValidationError(f"{path} has unsupported field(s): {', '.join(sorted(unknown))}")


def validate_copy(value: Any, path: str) -> None:
    copy = expect_object(value, path)
    reject_unknown_keys(copy, {"es", "en"}, path)
    for locale in ("es", "en"):
        entry = expect_object(copy.get(locale), f"{path}.{locale}")
        reject_unknown_keys(entry, {"title", "description"}, f"{path}.{locale}")
        expect_string(entry.get("title"), f"{path}.{locale}.title")
        expect_string(entry.get("description"), f"{path}.{locale}.description")


def validate_asset(value: Any, path: str) -> None:
    asset = expect_object(value, path)
    reject_unknown_keys(asset, {"url", "bytes", "sha256"}, path)
    url = expect_string(asset.get("url"), f"{path}.url")
    if not url.startswith("https://"):
        raise ValidationError(f"{path}.url must use HTTPS")
    expect_positive_int(asset.get("bytes"), f"{path}.bytes")
    sha256 = expect_string(asset.get("sha256"), f"{path}.sha256")
    if not SHA256_PATTERN.fullmatch(sha256):
        raise ValidationError(f"{path}.sha256 must be a lowercase 64-character SHA-256")


def validate_reference_ids(values: Any, allowed: set[str], path: str) -> None:
    ids = expect_list(values, path)
    if not ids:
        raise ValidationError(f"{path} must not be empty")
    for index, identifier in enumerate(ids):
        identifier = validate_id(identifier, f"{path}[{index}]")
        if identifier not in allowed:
            raise ValidationError(f"{path}[{index}] references unknown id '{identifier}'")


def validate_objective(value: Any, path: str, character_ids: set[str], tournament_ids: set[str]) -> None:
    objective = expect_object(value, path)
    reject_unknown_keys(objective, {"event", "target", "filters", "round"}, path)
    event = expect_string(objective.get("event"), f"{path}.event")
    if event not in EVENTS:
        raise ValidationError(f"{path}.event '{event}' is not supported")
    expect_positive_int(objective.get("target"), f"{path}.target")

    if event == "tournament_round_reached":
        round_name = expect_string(objective.get("round"), f"{path}.round")
        if round_name not in ROUNDS:
            raise ValidationError(f"{path}.round '{round_name}' is not supported")
    elif "round" in objective:
        raise ValidationError(f"{path}.round only applies to tournament_round_reached")

    filters = objective.get("filters", {})
    filters = expect_object(filters, f"{path}.filters")
    reject_unknown_keys(filters, {"player_character_ids", "game_modes", "tournament_ids"}, f"{path}.filters")
    if "player_character_ids" in filters:
        validate_reference_ids(filters["player_character_ids"], character_ids, f"{path}.filters.player_character_ids")
    if "tournament_ids" in filters:
        validate_reference_ids(filters["tournament_ids"], tournament_ids, f"{path}.filters.tournament_ids")
    if "game_modes" in filters:
        modes = expect_list(filters["game_modes"], f"{path}.filters.game_modes")
        if not modes:
            raise ValidationError(f"{path}.filters.game_modes must not be empty")
        for index, mode in enumerate(modes):
            mode = expect_string(mode, f"{path}.filters.game_modes[{index}]")
            if mode not in GAME_MODES:
                raise ValidationError(f"{path}.filters.game_modes[{index}] has unsupported mode '{mode}'")
    if event in TOURNAMENT_EVENTS and "tournament_ids" not in filters:
        # A generic tournament achievement is valid; explicit tournament IDs remain optional.
        return


def validate_reward(value: Any, path: str) -> None:
    reward = expect_object(value, path)
    reject_unknown_keys(reward, {"type", "amount"}, path)
    if reward.get("type") != "coins":
        raise ValidationError(f"{path}.type must be 'coins' in schema v1")
    expect_positive_int(reward.get("amount"), f"{path}.amount")


def validate_timed_item(value: Any, path: str) -> tuple[dict[str, Any], datetime, datetime]:
    item = expect_object(value, path)
    starts_at = parse_utc(item.get("starts_at"), f"{path}.starts_at")
    ends_at = parse_utc(item.get("ends_at"), f"{path}.ends_at")
    if starts_at >= ends_at:
        raise ValidationError(f"{path}.starts_at must be earlier than ends_at")
    return item, starts_at, ends_at


def validate_liveops(liveops: dict[str, Any], content_catalog: dict[str, Any]) -> None:
    reject_unknown_keys(liveops, {"schema_version", "revision", "min_client_version", "updated_at", "seasons", "achievements"}, "liveops")
    if liveops.get("schema_version") != 1:
        raise ValidationError("liveops.schema_version must equal 1")
    expect_string(liveops.get("revision"), "liveops.revision")
    min_client_version = expect_string(liveops.get("min_client_version"), "liveops.min_client_version")
    if not VERSION_PATTERN.fullmatch(min_client_version):
        raise ValidationError("liveops.min_client_version must use major.minor.patch")
    parse_utc(liveops.get("updated_at"), "liveops.updated_at")

    character_ids = {entry.get("id") for entry in content_catalog.get("characters", []) if isinstance(entry, dict)}
    character_ids.update(content_catalog.get("character_overrides", {}).keys())
    character_ids = {identifier for identifier in character_ids if isinstance(identifier, str)}
    tournament_ids = {entry.get("id") for entry in content_catalog.get("tournaments", []) if isinstance(entry, dict)}
    tournament_ids = {identifier for identifier in tournament_ids if isinstance(identifier, str)}

    seen_ids: set[str] = set()
    seasons = expect_list(liveops.get("seasons"), "liveops.seasons")
    for season_index, raw_season in enumerate(seasons):
        season_path = f"liveops.seasons[{season_index}]"
        season, season_start, season_end = validate_timed_item(raw_season, season_path)
        reject_unknown_keys(season, {"id", "status", "starts_at", "ends_at", "sort_order", "copy", "art", "challenges"}, season_path)
        season_id = validate_id(season.get("id"), f"{season_path}.id")
        if season_id in seen_ids:
            raise ValidationError(f"duplicate id '{season_id}'")
        seen_ids.add(season_id)
        if season.get("status") not in {"scheduled", "published", "archived"}:
            raise ValidationError(f"{season_path}.status must be scheduled, published, or archived")
        if isinstance(season.get("sort_order"), bool) or not isinstance(season.get("sort_order"), int) or season["sort_order"] < 0:
            raise ValidationError(f"{season_path}.sort_order must be a non-negative integer")
        validate_copy(season.get("copy"), f"{season_path}.copy")
        if "art" in season:
            validate_asset(season["art"], f"{season_path}.art")

        challenges = expect_list(season.get("challenges"), f"{season_path}.challenges")
        for challenge_index, raw_challenge in enumerate(challenges):
            challenge_path = f"{season_path}.challenges[{challenge_index}]"
            challenge, challenge_start, challenge_end = validate_timed_item(raw_challenge, challenge_path)
            reject_unknown_keys(challenge, {"id", "cadence", "starts_at", "ends_at", "sort_order", "copy", "objective", "reward"}, challenge_path)
            challenge_id = validate_id(challenge.get("id"), f"{challenge_path}.id")
            if challenge_id in seen_ids:
                raise ValidationError(f"duplicate id '{challenge_id}'")
            seen_ids.add(challenge_id)
            if challenge.get("cadence") not in {"daily", "weekly", "season"}:
                raise ValidationError(f"{challenge_path}.cadence must be daily, weekly, or season")
            if challenge_start < season_start or challenge_end > season_end:
                raise ValidationError(f"{challenge_path} must stay inside its season date range")
            if isinstance(challenge.get("sort_order"), bool) or not isinstance(challenge.get("sort_order"), int) or challenge["sort_order"] < 0:
                raise ValidationError(f"{challenge_path}.sort_order must be a non-negative integer")
            validate_copy(challenge.get("copy"), f"{challenge_path}.copy")
            validate_objective(challenge.get("objective"), f"{challenge_path}.objective", character_ids, tournament_ids)
            validate_reward(challenge.get("reward"), f"{challenge_path}.reward")

    achievements = expect_list(liveops.get("achievements"), "liveops.achievements")
    for index, raw_achievement in enumerate(achievements):
        path = f"liveops.achievements[{index}]"
        achievement = expect_object(raw_achievement, path)
        reject_unknown_keys(achievement, {"id", "sort_order", "visibility", "copy", "objective", "reward"}, path)
        achievement_id = validate_id(achievement.get("id"), f"{path}.id")
        if achievement_id in seen_ids:
            raise ValidationError(f"duplicate id '{achievement_id}'")
        seen_ids.add(achievement_id)
        if achievement.get("visibility") not in {"visible", "hidden_until_unlocked"}:
            raise ValidationError(f"{path}.visibility must be visible or hidden_until_unlocked")
        if isinstance(achievement.get("sort_order"), bool) or not isinstance(achievement.get("sort_order"), int) or achievement["sort_order"] < 0:
            raise ValidationError(f"{path}.sort_order must be a non-negative integer")
        validate_copy(achievement.get("copy"), f"{path}.copy")
        validate_objective(achievement.get("objective"), f"{path}.objective", character_ids, tournament_ids)
        validate_reward(achievement.get("reward"), f"{path}.reward")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("live-content/catalog.json"))
    parser.add_argument("--liveops", type=Path, default=Path("live-content/liveops.json"))
    parser.add_argument("--schema", type=Path, default=Path("live-content/liveops.schema.json"))
    args = parser.parse_args()
    try:
        schema = load_json(args.schema)
        if "$schema" not in schema or "$defs" not in schema:
            raise ValidationError(f"{args.schema}: not a JSON Schema document")
        validate_liveops(load_json(args.liveops), load_json(args.catalog))
    except ValidationError as exc:
        print(f"LiveOps catalog validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"LiveOps catalog valid: {args.liveops}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
