# Save Schema Strategy

## Objetivo

Evitar que cambios de schema rompan silenciosamente los archivos persistidos en `user://`.

## Archivos cubiertos

- `user://progress.cfg`
- `user://audio_settings.cfg`
- `user://tournament_state.cfg`

## Convencion

- cada archivo persistido guarda `meta.schema_version`
- la version actual base es `1`
- un archivo sin `schema_version` se considera `legacy` y entra por migracion

## Politica de migracion

- `schema_version == 0`
  - se leen los campos legacy conocidos
  - se sanitizan valores
  - se reescribe el archivo con `schema_version = 1`
- `schema_version > 1` o schema desconocido
  - no se intenta interpretar a ciegas
  - el runtime resetea el estado correspondiente
  - el archivo se reescribe con un schema soportado

## Reglas por dominio

### Progress

- se migran `total_coins`, `win_streak`, `best_win_streak` y `pending_reward`
- un `pending_reward` legacy con bonus ya cobrado se marca `claimed`
- un `pending_reward` legacy abierto se marca `expired` al cargar para evitar dobles grants despues de reinicios

### Audio

- se migran `master_volume`, `music_volume`, `sfx_volume` y `muted`
- valores fuera de rango se clamplean al rango `0.0..1.0`

### Tournament

- se migran `selected_player_character`, `opponent_queue`, `current_round_index`, `defeated_opponents`, `tournament_status`, `active_cup` y `last_result`
- si el payload no puede continuar de forma valida, se resetea el torneo en lugar de dejar progreso corrupto

## Cuando subir la version

Sube `CURRENT_SCHEMA_VERSION` solo cuando cambie el contrato persistido de manera incompatible.

Antes de subirla:

1. decidir si la migracion es posible o si conviene invalidar
2. implementar la rama de migracion explicita
3. actualizar este documento
4. correr smoke tests de persistencia
