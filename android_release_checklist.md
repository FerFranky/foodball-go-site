# Android Release Checklist

## Objetivo

Validar una APK candidata en dispositivo Android real antes de promoverla a release candidate o release final.

## Datos de la corrida

- Fecha:
- Build:
- Commit:
- Dispositivo:
- Version Android:
- Tester:
- Resultado global: `PASS` / `FAIL` / `BLOCKED`

## Checklist minima

### Instalacion y arranque

- [ ] La APK instala sin errores.
- [ ] El icono y nombre de app se ven correctos en launcher.
- [ ] La app abre en landscape.
- [ ] Los splash no muestran artefactos visuales obvios.

### Jugabilidad base

- [ ] Se puede entrar a modo libre.
- [ ] Se puede entrar a torneo.
- [ ] Los controles tactiles responden.
- [ ] El partido termina sin crash.

### Audio e idioma

- [ ] El audio reproduce sin glitch evidente.
- [ ] El mute y los sliders se comportan bien.
- [ ] El idioma seleccionado se refleja en menus y HUD.

### Persistencia

- [ ] Las monedas persisten despues de cerrar y reabrir.
- [ ] El torneo en progreso persiste despues de cerrar y reabrir.
- [ ] La configuracion de audio persiste.
- [ ] La configuracion de idioma persiste.

### Pantallas de cierre

- [ ] El modal final de modo libre no se desborda.
- [ ] El modal final de torneo no reinicia avance por error.
- [ ] La pantalla de campeon se renderiza correctamente.

### Resultado

- [ ] La build queda apta para compartir como candidata.

## Complementos

- Para persistencia detallada usar [persistence_smoke_test.md](persistence_smoke_test.md).
- Para QA debug controlado usar [qa_reset_tools.md](qa_reset_tools.md).
