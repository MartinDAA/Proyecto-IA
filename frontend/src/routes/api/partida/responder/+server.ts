import { error, json } from '@sveltejs/kit';
import { backendFetch } from '#lib/server/backend.js';
import type { RequestHandler } from './$types';

// Reenvía la petición a FastAPI con el token de la sesión (la cookie es httpOnly).
export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.token) error(401, 'No autenticado');

	let response: Response;
	try {
		response = await backendFetch(
			'/api/partida/responder',
			{ method: 'POST', body: await request.text() },
			locals.token
		);
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}

	if (!response.ok) error(response.status, 'No se pudo registrar la respuesta.');
	return json(await response.json());
};
