import { error, redirect } from '@sveltejs/kit';
import { backendFetch } from '#lib/server/backend.js';
import type { Escenario } from '#lib/juego.js';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user) redirect(303, '/login');

	let response: Response;
	try {
		response = await backendFetch('/api/escenarios', {}, locals.token);
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}
	if (!response.ok) error(response.status, 'No se pudieron cargar los paisajes.');

	const escenarios: Escenario[] = await response.json();
	// Se eligen en el servidor para que la página no cambie al hidratarse.
	return { escenarios, inicio: Math.floor(Math.random() * escenarios.length) };
};
