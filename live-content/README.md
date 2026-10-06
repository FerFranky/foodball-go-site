# Live content

`catalog.json` is the public, versioned Foodball Go character catalog. It currently ships empty so the mobile client exercises its safe offline fallback until a reviewed character asset set is published.

## Publish a character

1. Add exactly seven PNG, WebP, or JPG files under `live-content/<stable-id>/`: `idle`, `run_1`, `run_2`, `jump`, `selection_default`, `selection_player`, and `selection_cpu`.
2. Calculate byte counts and SHA-256 values from the final uploaded files.
3. Add a `published` record to `catalog.json` with localized `name.es` and `name.en`, `sprite_scale`, a minimum client version, and HTTPS URLs rooted at this repository's Pages domain.
4. Open a PR. Review visual quality, hashes, path allowlist, total payload, Spanish and English names, and that no asset is executable content.
5. Merge only after validating the client against the exact Pages URL.

## Roll back or retire

- To roll back, restore a previous `catalog.json` revision and the matching files in a PR.
- To retire a character, set its `status` to `disabled`; do not delete its files until active tournament snapshot support is deployed.
- Never upload Godot scenes, PCKs, scripts, archives, binaries, secrets, keys, or production configuration to this directory.