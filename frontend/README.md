# Frontend — K'iti Yachay

Interfaz del juego construida con SvelteKit. Muestra los paisajes, los
pictogramas y las ayudas del agente, y reproduce los mensajes con voz pregrabada.
Toda la comunicación con la API se hace desde el servidor de SvelteKit.

Al abrir el juego, Uku (el oso) presenta el programa al adulto, sin audio, y luego
explica cómo jugar. Los controles del adulto se abren manteniendo presionado el
botón **Educador** de la cabecera durante un segundo: ajustes (perfil de ayuda y
elementos a evitar), cómo se ven los elementos del paisaje (visibles, siluetas u
ocultos) y el tema. Los ajustes se guardan en una cookie de sesión; no se guardan
datos del niño.

Los pictogramas de ARASAAC están guardados en `static/pictogramas/` y los audios en
`static/audio/`, así que el juego no depende de servicios externos.

## Requisitos

- [pnpm](https://pnpm.io/)
- Node.js 24 o superior (versión usada en desarrollo)
- El [backend](../backend/README.md) en ejecución

## Puesta en marcha

Desde esta carpeta:

```bash
pnpm install
pnpm dev          # http://localhost:5173
```

El backend debe estar disponible en `http://localhost:8000` (o en la URL que
indique `BACKEND_URL`).

## Variables de entorno

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `BACKEND_URL` | `http://localhost:8000` | URL base de la API de FastAPI. Se lee en el servidor. |

Se puede definir en un `.env` en esta carpeta. Para producción, recuerda usar un
adaptador de SvelteKit acorde al entorno de despliegue en lugar de
`adapter-auto`.

## Scripts

| Comando | Descripción |
| --- | --- |
| `pnpm dev` | Servidor de desarrollo. |
| `pnpm build` | Compila la aplicación. |
| `pnpm preview` | Sirve la compilación de producción. |
| `pnpm check` | Comprueba tipos con `svelte-check`. |
| `pnpm lint` | Ejecuta Prettier y ESLint. |
| `pnpm format` | Formatea el código con Prettier. |

## Rutas

| Ruta | Descripción |
| --- | --- |
| `/` | Pantalla principal: muestra tres paisajes y permite cambiarlos. |
| `/ajustes` | Ajustes del educador: perfil de ayuda y elementos a evitar. |
| `/jugar/[escenario]` | Inicia una partida y muestra las rondas del paisaje elegido. |
| `POST /api/partida/responder` | Reenvía la respuesta del jugador al backend. |

## Estructura

```
src/
├── routes/
│   ├── +layout.svelte        # cabecera y tema
│   ├── +page.svelte          # presentación y selección de paisaje
│   ├── ajustes/              # ajustes del educador
│   ├── jugar/[escenario]/    # partida
│   └── api/partida/responder # puente con FastAPI
├── lib/
│   ├── components/           # pictogramas, escena, frase, cabecera, guía y presentación
│   ├── guia.ts               # textos de Uku, presentación e iconos
│   ├── juego.ts              # tipos y utilidades del juego
│   ├── voz.ts                # audios pregrabados (y voz del navegador de respaldo)
│   ├── audio.json            # índice texto → audio
│   └── server/               # cliente de la API y cookie de ajustes
└── env.ts                    # definición de BACKEND_URL
static/
├── audio/                    # voz pregrabada con Piper
└── pictogramas/              # copia local de los pictogramas de ARASAAC
```

## Créditos

Pictogramas: Sergio Palao. Origen: [ARASAAC](https://arasaac.org).
Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España).
