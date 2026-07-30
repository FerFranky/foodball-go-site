# Repository Hygiene

## Objetivo

Mantener el repo libre de artefactos generados localmente para que el historial, los diffs y los workflows de CI se mantengan previsibles.

## Artefactos que no deben versionarse

- APKs generadas localmente
- `.idsig`
- bundles `.aab`
- checksums generados para builds locales
- caches de Python como `__pycache__`
- salidas locales de CI como `build/`, `.android-sdk/` o `.config/`

## Regla operativa

Si un archivo puede regenerarse de forma determinista desde el repo y el pipeline, no debe vivir versionado salvo que sea un asset fuente del juego.

## Aplicacion actual

`.gitignore` ahora cubre:

- `build/`
- `.android-sdk/`
- `.config/`
- `*.apk`
- `*.aab`
- `*.idsig`
- `*.sha256`
- `__pycache__/`
- `*.pyc`

## Excepciones

- `export_presets.cfg` si se versiona porque define el preset fuente.
- assets reales del juego dentro de `assets/`.
- documentacion y scripts operativos del pipeline.
