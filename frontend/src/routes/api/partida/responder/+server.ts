import { error, json } from '@sveltejs/kit';
import { backendFetch } from '#lib/server/backend.js';
import type { RequestHandler } from './$types';

// Reenvía la petición a FastAPI, cuya dirección solo conoce el servidor.
export const POST: RequestHandler = async ({ request }) => {
	let response: Response;
	try {
		response = await backendFetch('/api/partida/responder', {
			method: 'POST',
			body: await request.text()
		});
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}

	if (!response.ok) error(response.status, 'No se pudo registrar la respuesta.');
	return json(await response.json());
};
