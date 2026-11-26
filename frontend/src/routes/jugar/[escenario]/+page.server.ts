import { error } from '@sveltejs/kit';
import { leerAjustes } from '#lib/server/ajustes.js';
import { backendFetch } from '#lib/server/backend.js';
import { VISTAS, type Turno, type Vista } from '#lib/juego.js';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, cookies }) => {
	let response: Response;
	try {
		response = await backendFetch('/api/partida/iniciar', {
			method: 'POST',
			body: JSON.stringify({ escenario_id: params.escenario, ...leerAjustes(cookies) })
		});
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}
	if (response.status === 404) error(404, 'Ese paisaje no existe.');
	if (response.status === 409) error(409, (await response.json()).detail);
	if (!response.ok) error(response.status, 'No se pudo iniciar la partida.');

	const vista = cookies.get('vista') ?? '';
	return {
		turno: (await response.json()) as Turno,
		vista: (Object.hasOwn(VISTAS, vista) ? vista : 'visibles') as Vista
	};
};
