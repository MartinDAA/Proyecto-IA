# K'iti Yachay

Juego educativo con pictogramas para practicar la descripción de lugares. El
agente muestra un paisaje, pregunta qué elementos contiene y guía al jugador con
pistas cuando se equivoca. Está pensado para niños y niñas de 5 a 15 años con
trastorno del espectro autista (nivel 2 o 3) y dificultades en la descripción
espacial.

El repositorio agrupa dos proyectos independientes, cada uno con sus propias
dependencias, configuración y documentación.

## Estructura

| Carpeta | Contenido | Documentación |
| --- | --- | --- |
| [`backend/`](backend/) | API FastAPI, motor del agente y banco de escenarios (Python + uv). | [README del backend](backend/README.md) |
| [`frontend/`](frontend/) | Interfaz SvelteKit con pictogramas y voz (TypeScript + pnpm). | [README del frontend](frontend/README.md) |
| [`docs/`](docs/) | Informe, plan de IA y despliegue, explicación del CSP y del algoritmo genético, y comandos de arranque. | [Plan](docs/PLAN_IA_Y_DESPLIEGUE.md) |

## Qué hace cada parte

El frontend muestra y reproduce; el backend decide y lleva el estado de la partida.
Toda la inteligencia artificial (el CSP de las opciones y la tabla de ayudas del
algoritmo genético) está en el backend.

| | Frontend (SvelteKit) | Backend (FastAPI) |
| --- | --- | --- |
| Papel | Muestra y reproduce | Decide y lleva el estado |
| Paisajes | Los dibuja | Define cuáles hay y qué contiene cada uno |
| Opciones de cada ronda | Las muestra | **Las elige con el CSP** (AC-3 y backtracking) |
| Respuesta del niño | Envía el pictograma tocado | Comprueba si es correcto y retira la opción equivocada |
| Ayuda tras un error | Resalta, muestra la pista o destaca la respuesta | **Decide qué ayuda dar** según la tabla del algoritmo genético y el perfil |
| Mensajes de Uku | Los muestra y los hace sonar | Arma la frase en pictogramas y el texto |
| Final | Muestra el resumen | Calcula la frase final, la estrella y lo que «no va aquí» |
| Ajustes del educador | Los guarda en una cookie y los envía | Aplica el perfil y los elementos a evitar |

## Puesta en marcha

Requisitos: [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/) y Node.js 24+.

En una terminal:

```bash
cd backend
uv sync
uv run fastapi dev      # http://localhost:8000
```

En otra:

```bash
cd frontend
pnpm install
pnpm dev                # http://localhost:5173
```

No hace falta iniciar sesión. El frontend usa
`http://localhost:8000` como backend por defecto; se puede cambiar con
`BACKEND_URL`.

## Créditos

Pictogramas: Sergio Palao. Origen: [ARASAAC](https://arasaac.org).
Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España).
