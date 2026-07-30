# Android Permission Posture

## Objetivo

Fijar la postura minima de permisos Android para el MVP y evitar que el pipeline publique builds con capacidades que el juego no necesita.

## Principio

Foodball Go MVP debe operar sin red, sin acceso a datos personales y sin sensores sensibles del dispositivo.

## Permisos que deben seguir en `false`

- `permissions/internet`
- `permissions/access_network_state`
- `permissions/access_wifi_state`
- `permissions/read_external_storage`
- `permissions/write_external_storage`
- `permissions/manage_external_storage`
- `permissions/record_audio`
- `permissions/camera`
- `permissions/post_notifications`

## Justificacion

- No hay backend productivo en alcance MVP.
- No hay captura de audio o camara en gameplay.
- No hay necesidad de leer almacenamiento del usuario.
- No hay funcionalidad de push notifications en el alcance actual.

## Aplicacion en CI

`scripts/ci/validate_project.py` falla si alguno de esos permisos cambia a `true`.

## Regla para cambios futuros

Si un feature nuevo requiere alguno de estos permisos:

1. Abrir issue de producto y seguridad.
2. Justificar por que el permiso es necesario.
3. Actualizar esta politica y el validador de CI en el mismo cambio.
