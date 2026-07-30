# QA Reset Tools

## Objetivo

Permitir pruebas repetibles sin borrar archivos manualmente dentro de `user://`.

## Switch de activacion

Las herramientas QA no aparecen solo por correr una build `debug`.

- Config actual: `project.godot`
- Ruta: `foodball/qa_tools_enabled`
- Default: `false`

Con `false`, la UI se comporta como un player normal.
Con `true`, una build `debug` muestra las herramientas QA en pausa.

## Como usarlo

1. Activa `foodball/qa_tools_enabled=true`.
2. Corre una build `debug`.
3. Entra a cualquier partido.
4. Abre pausa.
5. Usa la seccion `QA TOOLS`.

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
