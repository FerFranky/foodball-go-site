# Posada del gol — Navidad 2026

Issue #37. Depende del personaje #36 / PR #38. Fusionar primero ese PR.

- ID estable: `navidad_2026`.
- Inicio: **1 de diciembre de 2026, 00:00 America/Mexico_City**.
- Último día completo: **6 de enero de 2027**.
- UTC: `[2026-12-01T06:00:00Z, 2027-01-07T06:00:00Z)`.
- Las ventanas son inclusivas al inicio y exclusivas al final en el juego.

`status: published` habilita el contenido, pero la ventana impide activación y
conteo antes del inicio. Se usa published con fecha futura porque scheduled en
el cliente actual solo permite vista previa y no cambia solo a published.
Antes del inicio debe verse el contador hacia Posada del gol, sin sus retos ni
progreso. El manifiesto se actualiza independientemente de personajes.

## Retos

| Cadencia | Objetivo | Monedas |
| --- | --- | --- |
| Diario | 5 goles en Modo libre | 20 |
| Diario | 2 partidos completados en cualquier modo | 15 |
| Diario | 1 victoria en Modo libre | 20 |
| Semanal | 3 victorias en cualquier modo | 60 |
| Semanal | 2 victorias en Mexican Food | 90 |
| Temporada | 15 goles con Don Ponchito | 140 |
| Temporada | Ganar Mexican Food | 250 |
| Temporada | 30 goles en cualquier modo | 180 |
| Temporada | 10 victorias en cualquier modo | 200 |
| Temporada | 2 autogoles | 80 |

Cada objetivo reutiliza evento, dificultad y recompensa de Día de Muertos, sin
nueva economía. IDs independientes prefijados `navidad_`; no reutiliza progreso.
Las tres misiones diarias se reinician diariamente y las dos semanales por semana
según los periodos **UTC del cliente existente**. No son un pool aleatorio: se
renuevan los mismos tres/dos objetivos. Los cinco de temporada duran la ventana
completa. No cambia el sistema de reset a medianoche local.

Se conservan intactos los logros permanentes y las temporadas anteriores,
incluyendo IDs, ventanas y recompensas. No se borra progreso ni se activa la
temporada de prueba antigua. El personaje está disponible al publicar su propio
catálogo; no se oculta al acabar esta temporada.

## Pruebas

- Validación de LiveOps y catálogo, suite Python completa.
- Regresión 3/2/5, recompensas/objetivos comparados con la temporada anterior,
  referencia al personaje y ventanas exactas compartidas por sus diez retos.
- Límites: antes del 1 de diciembre, inicio, último segundo del 6 de enero y
  cierre del 7 de enero a medianoche de Ciudad de México.
- Parser del juego: manifiesto real muestra la próxima temporada y no registra
  sus retos antes del inicio; copia de prueba con fechas activas registra diez.

No se publica ni fusiona automáticamente. Requiere deploy correcto de Pages;
prueba física Android pendiente. No requiere AAB nuevo para el cliente vigente.
