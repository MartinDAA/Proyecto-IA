import { error, redirect } from '@sveltejs/kit';
import { backendFetch } from '#lib/server/backend.js';
import type { Turno } from '#lib/juego.js';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user) redirect(303, '/login');

	let response: Response;
	try {
		response = await backendFetch(
			'/api/partida/iniciar',
			{ method: 'POST', body: JSON.stringify({ escenario_id: params.escenario }) },
			locals.token
		);
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}
	if (response.status === 404) error(404, 'Ese paisaje no existe.');
	if (!response.ok) error(response.status, 'No se pudo iniciar la partida.');

	return { turno: (await response.json()) as Turno };
};
