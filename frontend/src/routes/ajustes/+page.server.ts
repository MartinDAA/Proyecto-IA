import { error, fail, redirect } from '@sveltejs/kit';
import { guardarAjustes, leerAjustes } from '#lib/server/ajustes.js';
import { backendFetch } from '#lib/server/backend.js';
import type { Escenario, Perfil } from '#lib/juego.js';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	let respuestas: Response[];
	try {
		respuestas = await Promise.all([
			backendFetch('/api/perfiles'),
			backendFetch('/api/escenarios')
		]);
	} catch {
		error(503, 'No se pudo conectar con el servidor.');
	}
	if (respuestas.some((r) => !r.ok)) error(502, 'No se pudieron cargar los ajustes.');

	const perfiles: Perfil[] = await respuestas[0].json();
	const escenarios: Escenario[] = await respuestas[1].json();
	return { perfiles, escenarios, ajustes: leerAjustes(cookies) };
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const perfil = data.get('perfil');
		if (typeof perfil !== 'string' || !perfil) return fail(400, { error: 'Elige un perfil.' });
		guardarAjustes(cookies, { perfil, evitar: data.getAll('evitar').map(String) });
		redirect(303, '/');
	}
};
