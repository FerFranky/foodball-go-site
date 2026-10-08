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
- `content_rating` admite únicamente `all_ages`, `family` o `everyone`, porque
  Foodball Go está clasificado para público familiar.
- `contexts` acepta `free_play`, `tournament` y `album`. Omitirlo mantiene los
  tres contextos para compatibilidad; una lista vacía oculta al personaje.

El cliente rechaza valores malformados o clasificaciones no familiares antes de
descargar recursos. Al cambiar políticas, incrementa `revision` para invalidar
correctamente la caché del catálogo.

## Personajes locales existentes

Usa el objeto superior `character_overrides` para administrar Burger, Pizza,
Fries, Taco, Hotdog, Icecream, Nacho y Soda. Un override acepta los mismos
cuatro campos de política y, opcionalmente, `album_cards`. La política filtra
al personaje local, pero sus sprites de juego se conservan dentro de la app
como respaldo sin conexión.

Las tarjetas extra se descargan solo al abrir la página correspondiente del
álbum. Cada personaje puede tener de 1 a 48 tarjetas remotas adicionales.
