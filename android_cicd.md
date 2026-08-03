# Android CI/CD

## Objetivo

Definir un flujo reproducible de CI/CD para validar cambios, construir una APK candidata y publicar release candidates desde GitHub.

## Workflows incluidos

### `Lint`

Archivo: `.github/workflows/lint.yml`

Corre en:

- `pull_request`
- `workflow_dispatch`

Hace:

- lint estructural de YAML con `yamllint`
- lint de GitHub Actions con `actionlint`
- compilacion sintactica de `scripts/ci`

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

- `pull_request`
- `push` a `main` cuando cambian archivos relevantes del juego o CI
- `workflow_dispatch`

Hace:

- valida el repo
- instala Android SDK segun la ruta recomendada por Godot
- instala Android SDK Platform 36 y Build-Tools 36.0.0
- descarga Godot `4.3-stable` y sus export templates oficiales
- crea un debug keystore temporal
- escribe `editor_settings` para export Android en CI
- actualiza `export_presets.cfg` para el build actual
- exporta APK debug o release
- verifica con `aapt` que el artifact exportado declara `targetSdkVersion=36`
- publica APK y checksum como artifact
- publica la URL del artifact en el summary del run
- comenta la URL en el PR cuando corre por `pull_request`
- permite comentar la URL en un issue si `workflow_dispatch` recibe `issue_number`

### `Android Release Candidate`

Archivo: `.github/workflows/release-candidate.yml`

Corre en:

- `workflow_dispatch`

Hace:

- valida el repo
- exige secretos de firma release
- construye APK release firmada
- verifica que la APK release declara `targetSdkVersion=36`
- genera checksum SHA-256
- publica una GitHub Release con el APK adjunto

## Scripts de soporte

- `scripts/ci/validate_project.py`
- `scripts/ci/write_editor_settings.py`
- `scripts/ci/update_android_preset.py`
- `scripts/ci/validate_release_candidate.py`

## Flujo recomendado

1. Abrir PR.
2. Dejar pasar `Lint`.
3. Dejar pasar `PR Validation`.
4. Dejar pasar `Android Candidate Build` en PR.
5. Hacer merge a `main`.
6. Probar en dispositivo real con [android_release_checklist.md](android_release_checklist.md) y [persistence_smoke_test.md](persistence_smoke_test.md).
7. Cuando la candidata este aprobada, correr `Android Release Candidate`.

Si necesitas lanzar una candidata manual, ejecuta `Android Candidate Build` con `version_name`, `version_code`, `build_type` y opcionalmente `issue_number` para que el workflow deje la liga del artifact en ese issue.

## Notas

- La instalacion de Android SDK sigue la documentacion oficial de Godot para export Android.
- La exportacion usa `--headless --export-debug` o `--headless --export-release`, que Godot documenta como validos para automatizacion.
- La release candidate asume firma release via secretos del repositorio.
