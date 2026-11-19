import { BACKEND_URL } from '$app/env/private';

export const SESSION_COOKIE = 'session';

/** Llama a la API de FastAPI, añadiendo el token si se indica. */
export function backendFetch(path: string, init: RequestInit = {}, token?: string | null) {
	const headers = new Headers(init.headers);
	if (init.body) headers.set('Content-Type', 'application/json');
	if (token) headers.set('Authorization', `Bearer ${token}`);
	return fetch(`${BACKEND_URL}${path}`, { ...init, headers });
}
