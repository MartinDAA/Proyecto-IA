# Frontend — K'iti Yachay

Interfaz del juego construida con SvelteKit. Muestra los paisajes, los
pictogramas y las ayudas del agente, y reproduce los mensajes por voz. Toda la
comunicación con la API se hace desde el servidor: el token queda en una cookie
`httpOnly` y nunca llega al navegador.

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
| `/login` | Formulario de acceso; redirige al inicio si ya hay sesión. |
| `/jugar/[escenario]` | Inicia una partida y muestra las rondas del paisaje elegido. |
| `/logout` | Elimina la cookie de sesión y vuelve al inicio. |
| `POST /api/partida/responder` | Reenvía la respuesta del jugador al backend con el token de la sesión. |

## Flujo de autenticación

1. El formulario de `/login` envía usuario y contraseña al backend.
2. El token recibido se guarda en la cookie `session` (`httpOnly`, `sameSite=lax`,
   una hora de duración).
3. `src/hooks.server.ts` valida la cookie contra `/api/auth/me` en cada petición
   y deja el usuario y el token en `event.locals`.
4. Las páginas y la ruta interna de responder usan `backendFetch` para llamar a
   FastAPI añadiendo `Authorization: Bearer <token>`.

## Estructura

```
src/
├── routes/
│   ├── +layout.svelte        # cabecera y tema
│   ├── +page.svelte          # selección de paisaje
│   ├── login/                # inicio de sesión
│   ├── jugar/[escenario]/    # partida
│   ├── logout/               # cierre de sesión
│   └── api/partida/responder # puente con FastAPI
├── lib/
│   ├── components/           # pictogramas, escena, frase y cabecera
│   ├── juego.ts              # tipos y utilidades del juego
│   ├── voz.ts                # síntesis de voz del navegador
│   └── server/backend.ts     # cliente de la API con el token de sesión
├── hooks.server.ts           # carga de la sesión en cada petición
└── env.ts                    # definición de BACKEND_URL
```

## Créditos

Pictogramas: Sergio Palao. Origen: [ARASAAC](https://arasaac.org).
Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España).
