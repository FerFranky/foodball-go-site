# Persistence Smoke Test Checklist

## Objetivo

Validar en una build candidata que el estado critico del juego se guarda, se recupera y no se corrompe entre reinicios normales del app.

## Alcance

Esta corrida cubre:

- primer arranque
- progreso y monedas
- torneo en curso
- idioma
- audio
- recompensa posterior al partido
- reinicio controlado para repetir pruebas

## Prerrequisitos

- Build candidata instalada en un dispositivo Android real.
- Ejecutar en landscape.
- Tener acceso a una build `debug` si se quiere preparar corridas limpias con [qa_reset_tools.md](qa_reset_tools.md).
- Si la corrida es sobre una build release, reinstalar la app o limpiar almacenamiento antes de iniciar.

## Datos de la corrida

- Fecha:
- Build:
- Dispositivo:
- Version Android:
- Tester:
- Resultado global: `PASS` / `FAIL` / `BLOCKED`

## Criterio general de pase

- Ningun archivo persistido se pierde tras cerrar y volver a abrir la app.
- El juego retoma idioma, audio, torneo y monedas segun el ultimo estado confirmado.
- No aparecen crashes, pantallas rotas ni reseteos silenciosos.

## Preparacion recomendada

1. Si la build es `debug` y el switch `foodball/qa_tools_enabled=true` esta activo, abrir un partido.
2. Abrir pausa.
3. Ejecutar `QA RESET TOTAL`.
4. Cerrar y reabrir la app para empezar desde estado cero.
5. Si se esta validando una migracion, revisar la estrategia en [save_schema.md](save_schema.md).

## Checklist

### 1. Primer arranque limpio

- [ ] La app abre sin crash ni pantallas corruptas.
- [ ] Se muestra el flujo inicial esperado.
- [ ] El idioma por default es el esperado para la build.
- [ ] No existe progreso previo visible de torneo.
- [ ] El total de monedas inicial coincide con una corrida limpia.

Pasa si:
- La app arranca limpia y consistente sin arrastrar estado viejo.

### 2. Persistencia de dificultad y duracion de partido

1. Cambiar dificultad.
2. Cambiar duracion de partido.
3. Salir al menu.
4. Cerrar la app completamente.
5. Reabrir la app.

- [ ] La dificultad sigue seleccionada.
- [ ] La duracion sigue seleccionada.
- [ ] El texto de UI refleja los valores restaurados.

Pasa si:
- `settings.cfg` se restaura sin perder cambios del usuario.

### 3. Persistencia de idioma

1. Cambiar de idioma.
2. Navegar entre menu principal, torneo y partido.
3. Cerrar la app completamente.
4. Reabrir la app.

- [ ] El idioma se aplica en menus.
- [ ] El idioma se aplica en HUD y overlays.
- [ ] El idioma persiste tras reinicio.

Pasa si:
- Todo el texto relevante reaparece en el idioma seleccionado al relanzar.

### 4. Persistencia de audio

1. Ajustar volumen general.
2. Ajustar musica.
3. Ajustar efectos.
4. Activar o desactivar mute.
5. Cerrar la app completamente.
6. Reabrir la app.

- [ ] Los valores de audio se restauran.
- [ ] El estado de mute se conserva.
- [ ] La musica reproduce o se silencia acorde al estado restaurado.

Pasa si:
- `audio_settings.cfg` reaplica exactamente la ultima configuracion guardada.

### 5. Persistencia de monedas y recompensa base

1. Jugar un partido libre hasta terminar.
2. Anotar el total de monedas antes del partido.
3. Anotar monedas ganadas al final.
4. Volver al menu.
5. Cerrar y reabrir la app.

- [ ] El total de monedas aumenta conforme al resultado mostrado.
- [ ] El total persiste tras reinicio.
- [ ] No se duplica la recompensa por solo reabrir la app.

Pasa si:
- `progress.cfg` conserva el total correcto sin regalar monedas extra.

### 6. Recompensa post partido no reclamada

1. Terminar un partido.
2. Dejar visible el modal final sin reclamar bonus adicional.
3. Cerrar la app completamente.
4. Reabrir la app y revisar el total de monedas.

- [ ] El total de monedas no sube de forma silenciosa al relanzar.
- [ ] La recompensa base ya aplicada sigue presente.
- [ ] No se observa duplicado del bonus pendiente.

Pasa si:
- El pending reward no genera duplicacion por reinicio.

### 7. Torneo en progreso

1. Iniciar torneo.
2. Ganar al menos una ronda sin completar la copa.
3. Salir correctamente al torneo o al menu.
4. Cerrar la app completamente.
5. Reabrir la app.

- [ ] El torneo sigue disponible para continuar.
- [ ] Se conserva la ronda alcanzada.
- [ ] Se conserva el rival siguiente.
- [ ] Los marcadores de progreso coinciden con lo avanzado.

Pasa si:
- `tournament_state.cfg` restaura el avance sin mandar al inicio.

### 8. Reintento de torneo con costo

1. Perder una ronda de torneo.
2. Verificar costo de reintento.
3. Pagar reintento.
4. Confirmar que conserva el avance del torneo.
5. Cerrar y reabrir la app.

- [ ] Se descuentan monedas una sola vez.
- [ ] El torneo conserva el avance esperado.
- [ ] Tras relanzar, el estado sigue consistente.

Pasa si:
- El flujo de reintento no reinicia de mas ni rompe persistencia de monedas.

### 9. Cambio de idioma con torneo guardado

1. Dejar un torneo en progreso.
2. Cambiar idioma.
3. Cerrar y reabrir la app.
4. Volver a torneo.

- [ ] El torneo sigue en progreso.
- [ ] La UI se ve en el nuevo idioma.
- [ ] El progreso no se pierde por el cambio de idioma.

Pasa si:
- Ajustes de localizacion y estado de torneo conviven sin pisarse.

### 10. Corrida de cierre

- [ ] No hay bloqueos al regresar entre menu, torneo y partido.
- [ ] No hay textos mezclados entre idiomas.
- [ ] No hay audio trabado tras reinicios.
- [ ] No hay reseteo espontaneo de monedas o progreso.

Pasa si:
- La build puede considerarse candidata para una validacion mas amplia.

### 11. Migracion de save legacy

1. Instalar una build o usar datos creados antes del schema versionado.
2. Abrir la app.
3. Confirmar que progreso, audio y torneo siguen legibles o se resetean de forma controlada.
4. Cerrar la app.
5. Reabrir la app.

- [ ] La app no crashea al leer datos legacy.
- [ ] Los datos compatibles se migran y siguen utilizables.
- [ ] Un save invalido o incompatible no deja estado roto.
- [ ] Tras reabrir, el estado ya queda estable en el nuevo schema.

Pasa si:
- La migracion o invalidacion ocurre de forma controlada y no deja corrupcion silenciosa.

## Evidencia minima sugerida

- 1 captura del menu despues de reabrir la app con ajustes persistidos.
- 1 captura del torneo restaurado.
- 1 captura del modal final con monedas antes de cerrar.
- 1 nota corta por cada caso fallido con paso exacto y resultado observado.

## Registro de hallazgos

| Caso | Resultado | Evidencia | Nota |
| --- | --- | --- | --- |
| Primer arranque limpio |  |  |  |
| Persistencia de dificultad y duracion |  |  |  |
| Persistencia de idioma |  |  |  |
| Persistencia de audio |  |  |  |
| Persistencia de monedas y recompensa base |  |  |  |
| Recompensa post partido no reclamada |  |  |  |
| Torneo en progreso |  |  |  |
| Reintento de torneo con costo |  |  |  |
| Cambio de idioma con torneo guardado |  |  |  |
| Corrida de cierre |  |  |  |
| Migracion de save legacy |  |  |  |
