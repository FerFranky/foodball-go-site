# Mexican Food: ampliación de personajes

Revisión del catálogo: `2026-10-26.2`. Issue: #29.

| ID estable | Nombre | Directorio de assets |
| --- | --- | --- |
| `nopal` | Nopalín | `live-content/nopal/` |
| `elote_preparado` | Elote el Explosivo | `live-content/elote_preparado/` |
| `pozole` | Don Pozolazo | `live-content/pozole/` |
| `quesadilla` | Quesa la Traviesa | `live-content/quesadilla/` |
| `tamal` | Don Tamalón | `live-content/tamal/` |

Cada directorio contiene 8 WebP: `idle`, `run_1`, `run_2`, `jump`,
`selection_default`, `selection_player`, `selection_cpu` y `club`.
Los sprites tienen lienzo transparente de 512×341, altura visible de 300 px
y escala de cliente 0.44 (29 % mayor que la escala inicial de 0.34). Las selecciones son de 512×512 y la tarjeta de club
es de 512×768. Las variantes normal/jugador/CPU usan iluminación azul/verde/roja.
Se conserva el alfa generado y se comprime el arte para distribución remota.

Los cinco registros están publicados y habilitados para `free_play`,
`tournament` y `album`, con historias y textos en español e inglés.
Cada uno tiene una tarjeta de club de 140 monedas. El cargador actual exige
al menos una tarjeta válida para activar un personaje remoto.

La Copa Mexican Food queda formada por Taco, Nacho, Pancho de la Ofrenda,
Nopalín, Elote el Explosivo, Don Pozolazo, Quesa la Traviesa y Don Tamalón.
Los 8 participantes alcanzan el mínimo del cliente. No se modifica Fast Food.
Este contenido usa el contrato existente (`min_app_version: 1.0.11`):
su publicación se realiza al fusionar el PR y completar el deploy de Pages.

## Arte y prompts

Se usó la herramienta integrada de generación de imágenes, con una imagen
por asset, conservando la identidad de cada personaje como referencia en
las variantes. No se usaron placeholders ni se sustituyeron poses con copias.

Prompt base de sprites: “Single production 2D game sprite Foodball Go. Bold
black outlines, polished soft cartoon shading, cheerful expressive big eyes,
white gloves, black shorts and soccer cleats, three-quarter frontal facing
slightly right. Full body idle standing pose. Character is anthropomorphic
food itself. True transparent background. No scenery, floor, ground shadow,
ball, text, frame or watermark. Strong silhouette readable at 90px.”

Sujetos: nopal verde con pencas y uniforme verde oscuro; elote amarillo con
mayonesa, queso cotija y chile, uniforme naranja; tazón de pozole rojo con
maíz, lechuga, rábanos y limón; quesadilla dorada de media luna con queso,
pañuelo rojo y uniforme verde; tamal de masa dorada envuelto en hoja de maíz
abierta, uniforme rojo. Todos conservan guantes y calzado de fútbol.

Prompts de poses: preservar identidad y cambiar solamente brazos y piernas;
`run_1` usa zancada extendida, `run_2` una fase compacta con rodilla levantada
y pies debajo del cuerpo, `jump` ambas rodillas flexionadas y manos arriba.

Prompt de selección: conservar la identidad de la imagen base y usar la
selección de Churro como referencia exclusiva del marco metálico angular,
iluminación cian, fondo hexagonal y plataforma circular. Figura completa,
sin texto ni logotipos. Para jugador y CPU, preservar composición y personaje
y cambiar únicamente la iluminación a verde esmeralda o rojo rubí.

Prompt de álbum: “Portrait 2:3 collectible football club wallpaper card for
Foodball Go. Preserve exact mascot face, food body, uniform and colors.
Full-body character with soccer ball at feet on a green pitch in a Mexican
stadium, ornate metallic gold border with green-white-red accents,
floodlights and distant papel picado. No words, letters, numbers or logos.”

## Validación

- `python scripts/validate_catalog.py`: archivos, bytes, SHA-256, historias,
  referencias de copas y presupuesto de sincronización.
- `python scripts/validate_liveops.py` y sus pruebas existentes.
- Prueba aislada con el cargador de producción de Foodball Go
  (`e0f1b675d3efdfe5be7d13b758316c82abc79615`): se sustituyó solamente el
  transporte HTTP por lectura de los mismos archivos locales, comprobando
  integridad y decodificación. Pasaron la activación de los 7 remotos y
  la construcción de los 8 participantes de Mexican Food para cada uno
  de los cinco jugadores nuevos.

El paquete nuevo contiene 40 archivos y pesa 2,787,452 bytes. El presupuesto
completo de sprites/selecciones, incluidos Churro y Pancho, es de 2,634,166
bytes frente al límite de 32 MiB del juego. Las tarjetas se descargan bajo
demanda al consultar el álbum.
