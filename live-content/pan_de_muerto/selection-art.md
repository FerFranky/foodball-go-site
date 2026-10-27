# Selección de Pancho — revisión 2026-10-26.4

Corrección de Site #34 / juego #261: incorporar a Pancho a la línea gráfica
unificada sin cambiar sus sprites, escala, historia, álbum, precio ni copas.

| Normal | Jugador | CPU |
| --- | --- | --- |
| ![](pan_de_muerto_selection_default.webp) | ![](pan_de_muerto_selection_player.webp) | ![](pan_de_muerto_selection_cpu.webp) |

Tres WebP 512×512. Se generaron con la herramienta integrada de imágenes y
se optimizaron; los mismos bytes se integran en el cliente como respaldo.
Referencia de identidad: selección anterior de Pancho, inspeccionada antes
de editar. Referencia de estilo: `selection/Burger_default.webp` y contrato
visual del juego. Se inspeccionaron los tres outputs y las imágenes reducidas.
Pendiente revisión humana y prueba física del siguiente AAB.

## Prompts

Normal: “Use case: precise-object-edit / compositing. Foodball Go square
character-selection card. Preserve exactly Pancho's smiling face, brown eyes,
golden sugar bread and crossed bread bones, green-white-red Mexico jersey,
black shorts, white gloves, socks and green shoes. Identity reference is the
existing Pancho card. Use the renewed Burger card only for the thick angular
silver frame, saturated cyan blue hexagonal stadium, side floodlights and
circular platform. No burger parts. Center full body at roughly 75–80% height,
clear of the frame. Change environment/frame only, no text, logo or watermark.”

Variantes: “Use case: precise-object-edit. Preserve exactly Pancho's identity,
face, smile, bread/sugar, pose, proportions, clothing colors, accessories,
silver frame and all composition geometry of the new normal card. Change
only cyan blue environmental illumination in hexagons, inner border, lights
and platform to saturated emerald green for PLAYER / ruby red for CPU.
Square, full bleed, no text, numbers, logo, watermark or new elements.”

Validación: bytes/SHA-256 y dimensiones, catálogo/LiveOps y pruebas Python.
El cliente nuevo comprueba correspondencia con los assets integrados, carga
antes del menú y no solicita imágenes por HTTP si el hash ya está disponible
en la app o en la caché. Clientes anteriores siguen siendo compatibles y
obtienen estas tres tarjetas mediante su cargador de personajes existente.
