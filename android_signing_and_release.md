# Android Signing And Release

## Objetivo

Definir los secretos y el procedimiento minimo para firmar builds release de Android desde GitHub Actions sin exponer credenciales en el repo.

## Secretos requeridos

Configurar estos secretos a nivel repositorio:

- `ANDROID_RELEASE_KEYSTORE_BASE64`
- `ANDROID_RELEASE_KEYSTORE_ALIAS`
- `ANDROID_RELEASE_KEYSTORE_PASSWORD`

## Formato esperado

### `ANDROID_RELEASE_KEYSTORE_BASE64`

- Contiene el archivo `.keystore` o `.jks` codificado en base64.
- Se decodifica en tiempo de ejecucion dentro del runner.

### `ANDROID_RELEASE_KEYSTORE_ALIAS`

- Alias de la llave usada para firmar la APK release.

### `ANDROID_RELEASE_KEYSTORE_PASSWORD`

- Password del keystore y de la llave release.

## Modo debug vs release

### Debug

- El workflow genera un keystore temporal dentro del runner.
- Se usa para builds candidatas internas y validacion tecnica.
- No debe distribuirse como release externa.

### Release

- Requiere los secretos anteriores.
- Firma la APK con la identidad real del proyecto.
- Debe usarse para release candidates o entregables compartibles fuera del equipo.

## Rotacion recomendada

1. Guardar el keystore original en un vault fuera de GitHub.
2. Rotar secretos si alguien con acceso deja el proyecto.
3. Rotar secretos si el keystore fue expuesto o descargado fuera de control.
4. Probar una release candidate nueva inmediatamente despues de una rotacion.

## Publicacion de release candidate

El workflow `Android Release Candidate` pide:

- `release_tag`
- `version_name`
- `version_code`
- `prerelease`

Salida esperada:

- APK firmada
- checksum `.sha256`
- GitHub Release asociada al commit

## Reglas operativas

- No commitear rutas reales de keystore en el repo.
- No commitear passwords, alias sensibles o archivos `.jks`.
- No usar secretos personales para builds compartidas del proyecto.
- Toda release candidate debe quedar asociada a un tag y a un commit trazable.
