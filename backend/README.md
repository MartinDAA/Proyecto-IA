# Backend — K'iti Yachay

API en FastAPI que expone el juego y el motor de decisión del agente. El agente
pregunta por los elementos de un paisaje usando pictogramas, evalúa cada
respuesta y responde con una ayuda cuando el jugador se equivoca.

## Requisitos

- [uv](https://docs.astral.sh/uv/) (gestiona Python y las dependencias)
- Python 3.12 o superior (`.python-version` fija 3.12; uv lo instala si hace falta)

## Puesta en marcha

Desde esta carpeta:

```bash
uv sync
uv run fastapi dev      # http://localhost:8000 · documentación en /docs
```

Al arrancar se crea un usuario temporal **admin / admin** en memoria (solo para
desarrollo). Se puede cambiar con `SEED_ADMIN_USERNAME` y `SEED_ADMIN_PASSWORD`.

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

La ruta se busca automáticamente desde el código. Para usar otro archivo, define
`KITI_ESCENARIOS` con la ruta al JSON.

## Variables de entorno

Se leen desde el entorno o desde un archivo `.env` en esta carpeta.

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `SECRET_KEY` | clave de desarrollo | Clave para firmar los JWT. Cambiarla fuera de desarrollo. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Duración del token de acceso. |
| `CORS_ORIGINS` | `["http://localhost:5173", "http://localhost:4173"]` | Orígenes permitidos por CORS. |
| `SEED_ADMIN_USERNAME` | `admin` | Usuario temporal creado al arrancar. |
| `SEED_ADMIN_PASSWORD` | `admin` | Contraseña del usuario temporal. |
| `KITI_ESCENARIOS` | — | Ruta alternativa a `datos/escenarios.json`. |

## Endpoints

Las rutas protegidas requieren `Authorization: Bearer <token>`.

| Método | Ruta | Auth | Descripción |
| --- | --- | --- | --- |
| GET | `/api/health` | No | Comprueba que el servidor está activo. |
| POST | `/api/auth/login` | No | `{ username, password }` → `{ access_token, token_type }`. |
| GET | `/api/auth/me` | Sí | Devuelve el usuario del token. |
| GET | `/api/escenarios` | Sí | Lista los 10 paisajes con sus pictogramas. |
| POST | `/api/partida/iniciar` | Sí | `{ escenario_id }` → primer turno de la partida. |
| POST | `/api/partida/responder` | Sí | `{ partida_id, pictograma }` → turno siguiente, ayuda o resumen. |

## Tests y simulación

```bash
uv run pytest
uv run python -m ia_models.experimento_a                          # partida simulada
uv run python -m ia_models.experimento_a --escenario playa --semilla 7
```

`uv run python -m ia_models.herramientas.resolver_arasaac` completa los
identificadores de ARASAAC que falten en el JSON (modifica el archivo).

## Estructura

```
app/
├── main.py                  # app, CORS, routers y usuario temporal
├── dependencies.py          # inyección de dependencias y usuario autenticado
├── core/                    # configuración y seguridad (hash, JWT)
├── models/                  # modelos de dominio y esquemas de la API
├── repositories/            # interfaces de acceso a datos
│   └── implementations/     # implementaciones en memoria
├── services/                # lógica de negocio (auth y partida)
└── controllers/             # endpoints HTTP
ia_models/
├── escenarios.py            # carga y consulta del banco de escenarios
├── entorno.py               # estado de la partida y reglas de las rondas
├── agentes.py               # agente que elige la siguiente ayuda
├── generador.py             # mensajes en pictogramas y texto
├── simulador.py             # partidas automáticas para pruebas
├── experimento_a.py         # partida guiada por consola
└── herramientas/            # utilidades (resolver pictogramas de ARASAAC)
datos/escenarios.json        # banco de escenarios y catálogo de pictogramas
tests/                       # pruebas del motor y de la API
docs/Informe.docx            # informe académico del proyecto (Hito 1)
```

## Documentación

- [Informe del proyecto (Hito 1)](docs/Informe.docx): contexto, objetivos,
  modalidad de juego, catálogo de pictogramas y capturas.
- [README general del monorepo](../README.md)
- [Documentación del frontend](../frontend/README.md)
