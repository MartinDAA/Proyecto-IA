import type { Handle } from '@sveltejs/kit/hooks';
import { SESSION_COOKIE, backendFetch } from '#lib/server/backend.js';

export const handle: Handle = async ({ event, resolve }) => {
	event.locals.user = null;
	event.locals.token = null;

	const token = event.cookies.get(SESSION_COOKIE);
	if (token) {
		try {
			const response = await backendFetch('/api/auth/me', {}, token);
			if (response.ok) {
				event.locals.user = await response.json();
				event.locals.token = token;
			} else if (response.status === 401) {
				event.cookies.delete(SESSION_COOKIE, { path: '/' });
			}
		} catch {
			// Backend caído: se trata como no autenticado sin borrar la cookie.
		}
	}

	return resolve(event);
};
