import { error } from '@sveltejs/kit';
import { leerAjustes } from '#lib/server/ajustes.js';
import { backendFetch } from '#lib/server/backend.js';
import type { Escenario } from '#lib/juego.js';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	let response: Response;
	try {
		response = await backendFetch('/api/escenarios');
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}
	if (!response.ok) error(response.status, 'No se pudieron cargar los paisajes.');

	const { evitar } = leerAjustes(cookies);
	const escenarios = ((await response.json()) as Escenario[]).filter(
		(e) => !e.elementos.some((x) => evitar.includes(x.id))
	);
	// Se eligen en el servidor para que la página no cambie al hidratarse.
	return { escenarios, inicio: Math.floor(Math.random() * escenarios.length) };
};
