# Android CI/CD

## Objetivo

Definir un flujo reproducible de CI/CD para validar cambios, construir una APK candidata y publicar release candidates desde GitHub.

## Workflows incluidos

### `PR Validation`

Archivo: `.github/workflows/pr-validation.yml`

Corre en:

- `pull_request`
- `workflow_dispatch`

Hace:

- checkout del repo
- setup de Python
- validacion estructural del proyecto con `scripts/ci/validate_project.py`

Valida:

- `project.godot`
- `export_presets.cfg`
- iconos Android
- postura minima de permisos
- presencia de documentos operativos de Android y QA

### `Android Candidate Build`

Archivo: `.github/workflows/android-candidate.yml`

Corre en:

- `push` a `main` cuando cambian archivos relevantes del juego o CI
- `workflow_dispatch`

Hace:

- valida el repo
- instala Android SDK segun la ruta recomendada por Godot
- descarga Godot `4.3-stable` y sus export templates oficiales
- crea un debug keystore temporal
- escribe `editor_settings` para export Android en CI
- actualiza `export_presets.cfg` para el build actual
- exporta APK debug o release
- publica APK y checksum como artifact

### `Android Release Candidate`

Archivo: `.github/workflows/release-candidate.yml`

Corre en:

- `workflow_dispatch`

Hace:

- valida el repo
- exige secretos de firma release
- construye APK release firmada
- genera checksum SHA-256
- publica una GitHub Release con el APK adjunto

## Scripts de soporte

- `scripts/ci/validate_project.py`
- `scripts/ci/write_editor_settings.py`
- `scripts/ci/update_android_preset.py`

## Flujo recomendado

1. Abrir PR.
2. Dejar pasar `PR Validation`.
3. Hacer merge a `main`.
4. Dejar que `Android Candidate Build` genere la APK candidata.
5. Probar en dispositivo real con [android_release_checklist.md](android_release_checklist.md) y [persistence_smoke_test.md](persistence_smoke_test.md).
6. Cuando la candidata este aprobada, correr `Android Release Candidate`.

## Notas

- La instalacion de Android SDK sigue la documentacion oficial de Godot para export Android.
- La exportacion usa `--headless --export-debug` o `--headless --export-release`, que Godot documenta como validos para automatizacion.
- La release candidate asume firma release via secretos del repositorio.
