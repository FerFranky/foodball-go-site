# Catálogo de contenido vivo

Cada personaje publicado puede declarar su disponibilidad directamente en
`catalog.json`:

```json
{
  "enabled": true,
  "min_app_version": "1.0.11",
  "content_rating": "all_ages",
  "contexts": ["free_play", "tournament", "album"]
}
```

- `enabled` es booleano. Con `false`, el cliente no descarga assets ni muestra
  al personaje.
- `min_app_version` es la versión mínima del cliente. Se conserva
  `min_client_version` como alias de compatibilidad para catálogos anteriores.
- `content_rating` admite únicamente `all_ages`, `family` o `everyone`. Este
  campo describe la idoneidad del contenido del catálogo; no reemplaza la
  clasificación de audiencia de la app, que se administra en Google Play
  Console.
- `contexts` acepta `free_play`, `tournament` y `album`. Omitirlo mantiene los
  tres contextos para compatibilidad; una lista vacía oculta al personaje.

El cliente rechaza valores malformados o clasificaciones no compatibles antes
de descargar recursos. Al cambiar políticas, incrementa `revision` para
invalidar correctamente la caché del catálogo.

## Personajes locales existentes

Usa el objeto superior `character_overrides` para administrar Burger, Pizza,
Fries, Taco, Hotdog, Icecream, Nacho y Soda. Un override acepta los mismos
cuatro campos de política y, opcionalmente, `album_cards`. La política filtra
al personaje local, pero sus sprites de juego se conservan dentro de la app
como respaldo sin conexión.

Las tarjetas extra se descargan solo al abrir la página correspondiente del
álbum. Cada personaje puede tener de 1 a 48 tarjetas remotas adicionales.

## LiveOps: temporadas, retos y logros

`liveops.json` es un manifiesto independiente para contenido que cambia con el
tiempo. No se agregan temporadas a `catalog.json`: así una actualización de
retos no invalida la caché de personajes, torneos ni tarjetas.

URL pública contractual:

```text
https://ferfranky.github.io/foodball-go-site/live-content/liveops.json
```

El formato se describe en `liveops.schema.json` y se valida durante el deploy
de Pages mediante `scripts/validate_liveops.py`. El contrato inicial usa:

- una temporada con `id`, `status`, fechas UTC, textos `es`/`en`, orden y
  retos;
- retos de cadencia `daily`, `weekly` o `season`;
- logros permanentes con visibilidad normal u oculta hasta desbloquearse;
- objetivos de goles, autogoles, partidos, victorias, progreso de torneo y
  compra de stickers (`sticker_purchased`);
- filtros opcionales por personaje, modo (`free_play` o `tournament`), copa y
  tarjeta del álbum (`collectible_ids`);
- recompensas de monedas. El progreso y la reclamación se guardan en el juego,
  nunca en este sitio.

### Publicar o editar una temporada

1. Usa IDs minúsculos estables (`^[a-z0-9][a-z0-9_-]{2,63}$`). No reutilices
   un ID con otro significado.
2. Usa fechas ISO-8601 en UTC con sufijo `Z`. Las ventanas de los retos deben
   quedar dentro de la ventana de su temporada; diario y semanal se reinician
   en UTC.
3. Incluye `copy.es` y `copy.en`, y referencia únicamente personajes, torneos
   y tarjetas remotas existentes en `catalog.json`. Los IDs de tarjeta son los
   de `album_cards[].id`.
4. Para arte opcional, publica una URL HTTPS y su tamaño/sha256, igual que los
   assets de personajes.
5. Aumenta `revision` para todo cambio semántico. Conserva
   `schema_version: 1` para cambios compatibles; un cambio incompatible exige
   un nuevo esquema y soporte previo en el juego.
6. Ejecuta antes del PR:

   ```powershell
   python scripts/validate_liveops.py
   python -m unittest scripts/test_validate_liveops.py
   ```

Los tipos de objetivo nuevos se publican solo después de que una versión del
juego los soporte. Site no recolecta perfiles, ranking, telemetría ni datos
personales.
