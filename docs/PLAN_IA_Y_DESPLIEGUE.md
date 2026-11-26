# K'iti Yachay — Plan de IA y despliegue

Estado al 25/11/2026. Este documento resume lo decidido y lo pendiente para retomar el proyecto.

## 1. Estructura del proyecto

```
TP_1ASI404_9138_GRUPO_05/
├── backend/    FastAPI (repo git propio). IA en backend/ia_models/
│   └── datos/escenarios.json   ← banco de escenarios (movido aquí)
├── frontend/   SvelteKit (repo git propio). Llama al backend desde el servidor (BACKEND_URL)
└── docs/       Informe.docx, este archivo, ag_csp_explicado.html
```

IA actual: los distractores se eligen con un CSP (`ia_models/csp.py`, `Banco.distractores()`) y las
ayudas con `AgenteGenetico`, que lee `backend/datos/politicas.json` (una tabla por perfil).
`AgenteProgramado` (RESALTAR → PISTA → MODELAR) queda como línea base del Experimento B.

## 2. Despliegue (servidor gratuito)

### Decisión
No hacer monolito. Frontend y backend se despliegan por separado:
- **Frontend** en Vercel o Netlify (`adapter-auto` funciona sin cambios).
- **Backend** en Render, Koyeb o similar, con **1 solo worker** (las partidas viven en memoria).

Motivo: el frontend usa funciones de servidor (acciones de formulario, cookie httpOnly,
proxy de `/responder`); hacerlo monolito obliga a reescribirlo. Separados, cada uno tiene su
propia cuota gratuita.

### Hecho
- [x] `datos/` movido a `backend/datos/`. `ruta_escenarios()` lo encuentra solo. Tests: 15 pasan.
- [x] `frontend/src/routes/layout.css` ya no lee el JSON: las clases de Tailwind de los cielos
      están en `@source inline(...)`. **Si se agrega o cambia un `cielo`, actualizar esa lista.**

### Pendiente
- [x] Commit del estado anterior a la IA en la rama `ia-csp-ag` de ambos repos (sin push).
- [ ] Definir `BACKEND_URL` en el host del frontend (por defecto apunta a `http://localhost:8000`).
- [x] Login retirado por innecesario: ya no hacen falta `SECRET_KEY`, usuario semilla ni argon2.
- [ ] Si se publica en internet: la API queda abierta; limitar cuántas partidas se guardan a la vez.
- [x] (al iniciar otra partida; máx. 2 h) Borrar partidas terminadas o viejas en `InMemoryPartidaRepository` (antes nunca se borraban).
- [ ] Revisar `docs/Informe.docx` por referencias a la ruta vieja `datos/` (`arranque` no tiene).

### Riesgos conocidos
- El plan gratuito apaga el servidor tras ~15 min sin uso: el primer acceso tarda y se pierden
  las partidas en curso. Para la presentación, abrir la página unos minutos antes.
- Partidas en memoria: con más de 1 worker o tras un reinicio, `/api/partida/responder`
  devuelve 404 "No existe la partida".

## 3. Técnicas de IA del curso

Revisados los materiales de las semanas 1–4, 11, 12 y 13 (de las semanas 5, 6 y 9 solo hay
imágenes: redes neuronales y CNN).

| Tema | Uso en K'iti Yachay | Decisión |
|---|---|---|
| CSP: backtracking + AC-3 (sem. 13) | Elegir los 3 distractores de cada ronda | **Usar** |
| Algoritmo genético (sem. 3) | Optimizar la política de ayudas con el simulador, fuera del servidor | **Usar** |
| Hill climbing / recocido simulado (sem. 2, 4) | Alternativa al AG para la misma optimización | Opcional, para comparar |
| A* / ramificación y poda | Ordenar paisajes por dificultad | Descartado (encaje forzado) |
| NLP (sem. 11–12) | El niño no escribe texto | Descartado |
| CNN / redes neuronales | Reconocer fotos de lugares | Descartado (no cabe en servidor gratuito) |
| Ética (sem. 1) | Sección del informe | **Incluir en el informe** |

Explicación interactiva de ambas técnicas: `docs/ag_csp_explicado.html`
(publicada en https://claude.ai/artifact/4UQyZZQawEceqojwCky4n7).

## 4. Plan de integración (pensado para niños con TEA nivel 2–3)

**Implementado el 25/11/2026** (pasos 1, 2 y 3). Diferencias con el plan:
- No se agregó `confundibles`: el campo `compatibles`, que ya existía, cumple esa función.
- `ambiente` se asignó de forma **provisional** (agua, frio, calor, campo_ciudad): falta validarlo.
- La aptitud del AG es el puntaje esperado exacto (`jugador.py`), no simulado; un test comprueba que
  coincide con partidas simuladas.
- Perfiles: solo cambia la frustración por error (0.30 / 0.22 / 0.15).
- Si un elemento a evitar está en el paisaje, ese paisaje se oculta; si no quedan 3 distractores, se avisa.

| Perfil | Guion | AG (óptimo) | Abandonos guion → AG (simulado) |
|---|---|---|---|
| Se frustra con facilidad | 14.27 | 17.58 | 32.4 % → 9.7 % |
| Estándar | 17.33 | 19.00 | 24.6 % → 10.7 % |
| Autonomía | 20.23 | 21.55 | 17.2 % → 21.4 % (sube: nunca muestra la respuesta) |

Límites a mencionar en el informe: las probabilidades son inventadas, y la aptitud se separa por categoría
(27 combinaciones por categoría), así que el óptimo también se halla por fuerza bruta.

### Paso 1 — CSP de distractores
- Agregar a `backend/datos/escenarios.json`:
  - `ambiente` de cada uno de los 40 elementos (p. ej. agua, frío, calor, campo y ciudad).
  - `confundibles` de cada escenario: elementos que podrían estar ahí de verdad
    (p. ej. granja: pato, paloma).
- Reescribir `Banco.distractores()` en `backend/ia_models/escenarios.py` como CSP:
  - **Variables:** D1, D2, D3.
  - **Dominio:** elementos de la misma categoría.
  - **Unarias:** no es la respuesta; no está en `confundibles`; no está en la lista de evitar del educador.
  - **Binarias:** todos distintos; cada uno de un ambiente distinto.
  - Barajar el dominio con `rng` para variar las rondas. Si no hay solución, avisar o relajar la regla de ambientes.
- Agregar tests en `backend/tests/` (ronda válida, caso sin solución).
- **Bloqueante:** confirmar con la especialista las listas de `ambiente` y `confundibles`.
  Las de `ag_csp_explicado.html` son solo un ejemplo con animales.

### Paso 2 — Algoritmo genético offline
- Script en `backend/ia_models/herramientas/` que use `simulador.py` como fitness.
- **Cromosoma:** 12 genes = ayuda tras el error 1, 2 y 3 × 4 categorías. Valores: R, P, M.
- **Parámetros de la demo:** población 24, torneo de 3, cruce en un punto (0.9),
  mutación 0.06 por gen, elitismo 2.
- **Modelo de jugador de la demo** (inventado, hay que calibrarlo):
  - Acierta al primer intento con 0.35. Repetir la misma ayuda rinde un 40 % menos.
  - Probabilidad de acertar tras cada ayuda:

    | Ayuda | Animal | Construcción | Transporte | Objeto |
    |---|---|---|---|---|
    | Resaltar | 0.55 | 0.65 | 0.50 | 0.35 |
    | Pista | 0.70 | 0.45 | 0.50 | 0.30 |
    | Modelar | 1.00 | 1.00 | 1.00 | 1.00 |

  - Puntaje: +10 si acierta sin modelar, +3 si se modeló, −2 por error.
  - Abandono por frustración tras el error k: 0.22·k, con −6. Modelar evita el abandono.
  - Resultado: agente actual 17.33 vs. AG 19.00 (óptimo verificado probando las 3¹² políticas).
- Generar **una tabla por perfil**: baja tolerancia a la frustración, estándar, autonomía
  (cambian los pesos del fitness).
- Nuevo agente en `agentes.py` que lea la tabla del perfil en lugar de `GUION`.
- Comparar el agente programado con el agente AG en un "Experimento B", junto a `experimento_a.py`.

### Paso 3 — Configuración del educador (frontend)
- Pantalla previa para elegir el perfil y los elementos a evitar. Se envía al iniciar la
  partida (`/api/partida/iniciar`).

### Principios para el usuario con TEA
- **Predecibilidad:** la política de ayudas es fija por perfil y no cambia durante la partida.
- **Sin errores injustos:** nunca mostrar como distractor algo que podría estar en el paisaje.
- **El educador decide:** perfil y elementos a evitar, antes de jugar.
- **Privacidad:** no guardar datos por niño. Los perfiles se calculan de antemano.

## 5. Preguntas abiertas
- ¿Qué técnicas exige la rúbrica del TP? Revisar el enunciado antes de implementar.
- Listas de `ambiente` y `confundibles` para los 40 elementos (validar con la especialista).
- Probabilidades del jugador simulado: ¿se pueden estimar con la especialista?
