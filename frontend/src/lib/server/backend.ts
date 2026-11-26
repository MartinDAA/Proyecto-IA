import { BACKEND_URL } from '$app/env/private';

/** Llama a la API de FastAPI. */
export function backendFetch(path: string, init: RequestInit = {}) {
	const headers = new Headers(init.headers);
	if (init.body) headers.set('Content-Type', 'application/json');
	return fetch(`${BACKEND_URL}${path}`, { ...init, headers });
}
