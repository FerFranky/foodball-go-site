# Android Permission Posture

## Objetivo

Fijar la postura minima de permisos Android y evitar que el pipeline publique builds con capacidades que el juego no necesita.

## Principio

Foodball Go usa red exclusivamente para los anuncios recompensados de Google AdMob. No solicita acceso al almacenamiento del usuario, sensores sensibles ni permisos en tiempo de ejecucion.

`permissions/internet` debe estar en `true` mientras `[admob] enabled=true` en `project.godot`. Si AdMob se desactiva, CI exige que vuelva a `false`.

## Permisos que deben seguir en `false`

- `permissions/access_network_state`
- `permissions/access_wifi_state`
- `permissions/read_external_storage`
- `permissions/write_external_storage`
- `permissions/manage_external_storage`
- `permissions/record_audio`
- `permissions/camera`
- `permissions/post_notifications`

## Justificacion

- AdMob requiere conectividad para cargar anuncios recompensados. La integracion no usa un backend propio.
- No hay captura de audio o camara en gameplay.
- No hay necesidad de leer almacenamiento del usuario.
- No hay funcionalidad de push notifications en el alcance actual.

## Aplicacion en CI

`scripts/ci/validate_project.py` falla si algun permiso restringido cambia a `true`, o si el permiso de internet no coincide con el estado de AdMob.

## Regla para cambios futuros

Si un feature nuevo requiere alguno de estos permisos:

1. Abrir issue de producto y seguridad.
2. Justificar por que el permiso es necesario.
3. Actualizar esta politica y el validador de CI en el mismo cambio.
