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

El usuario de desarrollo es **admin / admin**. El frontend usa
`http://localhost:8000` como backend por defecto; se puede cambiar con
`BACKEND_URL`.

## Créditos

Pictogramas: Sergio Palao. Origen: [ARASAAC](https://arasaac.org).
Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España).
