# Backend — K'iti Yachay

API en FastAPI que expone el juego y el motor de decisión del agente. El agente
pregunta por los elementos de un paisaje usando pictogramas, evalúa cada
respuesta y responde con una ayuda cuando el jugador se equivoca.

Usa dos técnicas de IA:

- **CSP (AC-3 + backtracking)** para elegir los 3 distractores de cada ronda: distintos,
  de ambientes distintos y nunca algo que podría estar en el paisaje ni que el
  educador pidió evitar (`ia_models/csp.py`, `Banco.distractores()`).
- **Algoritmo genético**, ejecutado fuera del servidor, para calcular qué ayuda dar
  tras cada error según el perfil del niño (`ia_models/herramientas/entrenar_politicas.py`).
  El resultado queda en `datos/politicas.json` y lo usa `AgenteGenetico`.

## Requisitos

- [uv](https://docs.astral.sh/uv/) (gestiona Python y las dependencias)
- Python 3.12 o superior (`.python-version` fija 3.12; uv lo instala si hace falta)

## Puesta en marcha

Desde esta carpeta:

```bash
uv sync
uv run fastapi dev      # http://localhost:8000 · documentación en /docs
```

La API no requiere autenticación.

## Datos del juego

El banco de escenarios vive en [`datos/escenarios.json`](datos/escenarios.json) y
contiene tres bloques:

- `pictogramas`: catálogo de pictogramas (nombre, emoji e identificador de ARASAAC).
  Incluye los 40 elementos del juego, los 10 paisajes, los 14 pictogramas de
  comunicación (función y categorías) y 37 pictogramas de apoyo para las pistas.
- `categorias`: las cuatro categorías que se juegan en orden: animal,
  construcción, transporte y objeto.
- `escenarios`: los 10 paisajes, cada uno con su objetivo (un elemento por
  categoría) y una lista de elementos `compatibles` que nunca se usan como
  distractores.

Cada elemento tiene un `ambiente` (agua, frio, calor o campo_ciudad) que usa el CSP.
Las listas de `ambiente` y `compatibles` son provisionales: falta validarlas con la
especialista. `datos/politicas.json` guarda la tabla de ayudas de cada perfil.

La ruta se busca automáticamente desde el código. Para usar otro archivo, define
`KITI_ESCENARIOS` con la ruta al JSON.

## Variables de entorno

Se leen desde el entorno o desde un archivo `.env` en esta carpeta.

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `CORS_ORIGINS` | `["http://localhost:5173", "http://localhost:4173"]` | Orígenes permitidos por CORS. |
| `KITI_ESCENARIOS` | — | Ruta alternativa a `datos/escenarios.json`. |

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/health` | Comprueba que el servidor está activo. |
| GET | `/api/escenarios` | Lista los 10 paisajes con sus pictogramas. |
| GET | `/api/perfiles` | Lista los perfiles de ayuda que puede elegir el educador. |
| POST | `/api/partida/iniciar` | `{ escenario_id, perfil?, evitar? }` → primer turno de la partida. `perfil` es `estandar` por defecto; `evitar` es una lista de elementos que no deben aparecer. |
| POST | `/api/partida/responder` | `{ partida_id, pictograma }` → turno siguiente, ayuda o resumen. |

Las partidas viven en memoria: el servidor debe correr con un solo proceso, y se
descartan las terminadas y las de más de 2 horas.

## Tests y simulación

```bash
uv run pytest
uv run python -m ia_models.experimento_a                          # partida simulada
uv run python -m ia_models.experimento_a --escenario playa --semilla 7
uv run python -m ia_models.experimento_b                          # guion fijo contra algoritmo genético
```

Herramientas (se ejecutan solo cuando cambian los datos):

| Comando | Qué hace |
| --- | --- |
| `uv run python -m ia_models.herramientas.entrenar_politicas` | Vuelve a calcular `datos/politicas.json` con el algoritmo genético. |
| `uv run --with pillow python -m ia_models.herramientas.descargar_pictogramas` | Guarda los pictogramas de ARASAAC en `frontend/static/pictogramas/`. |
| `uv run --with piper-tts python -m ia_models.herramientas.generar_audios` | Genera la voz pregrabada (necesita ffmpeg y una voz de Piper en `.voces/`). |
| `uv run python -m ia_models.herramientas.resolver_arasaac` | Completa los identificadores de ARASAAC que falten en el JSON. |

## Estructura

```
app/
├── main.py                  # app, CORS y routers
├── dependencies.py          # inyección de dependencias
├── core/                    # configuración
├── models/                  # modelos de dominio y esquemas de la API
├── repositories/            # interfaces de acceso a datos
│   └── implementations/     # implementaciones en memoria
├── services/                # lógica de negocio de la partida
└── controllers/             # endpoints HTTP
ia_models/
├── escenarios.py            # carga y consulta del banco de escenarios
├── entorno.py               # estado de la partida y reglas de las rondas
├── csp.py                   # AC-3 y backtracking (distractores)
├── jugador.py               # jugador simulado y perfiles (aptitud del AG)
├── agentes.py               # agente programado y agente genético
├── generador.py             # mensajes en pictogramas y texto
├── simulador.py             # partidas automáticas para pruebas
├── experimento_a.py         # partida guiada por consola
├── experimento_b.py         # comparación de agentes
└── herramientas/            # algoritmo genético, pictogramas, voz y ARASAAC
datos/escenarios.json        # banco de escenarios y catálogo de pictogramas
datos/politicas.json         # tabla de ayudas por perfil (sale del AG)
tests/                       # pruebas del motor y de la API
```

## Documentación

- [README general del monorepo](../README.md)
- [Documentación del frontend](../frontend/README.md)
