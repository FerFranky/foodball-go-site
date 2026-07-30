# QA Reset Tools

## Objetivo

Permitir pruebas repetibles sin borrar archivos manualmente dentro de `user://`.

## Como usarlo

1. Corre una build `debug`.
2. Entra a cualquier partido.
3. Abre pausa.
4. Usa la seccion `QA TOOLS`.

## Acciones disponibles

- `QA +10 GOLES`: suma 10 goles al jugador local.
- `QA BORRAR TORNEO`: limpia el avance persistido del torneo.
- `QA BORRAR PROGRESO`: reinicia monedas, racha y recompensa pendiente.
- `QA RESET AUDIO`: restaura audio a valores base.
- `QA RESET TOTAL`: limpia torneo, progreso, audio y ajustes de juego para volver a estado cero.

## Procedimiento corto para prueba limpia

1. Abrir pausa en una build `debug`.
2. Pulsar `QA RESET TOTAL`.
3. Volver a entrar al flujo que se quiera probar desde menu.

Con eso QA evita borrar archivos locales a ciegas y puede repetir pruebas desde un estado consistente.
