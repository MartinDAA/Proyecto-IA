import { fail, redirect } from '@sveltejs/kit';
import { dev } from '$app/env';
import { SESSION_COOKIE, backendFetch } from '#lib/server/backend.js';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = ({ locals }) => {
	if (locals.user) redirect(303, '/');
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const username = String(data.get('username') ?? '').trim();
		const password = String(data.get('password') ?? '');

		if (!username || !password) {
			return fail(400, { username, error: 'Escribe tu usuario y contraseña.' });
		}

		let response: Response;
		try {
			response = await backendFetch('/api/auth/login', {
				method: 'POST',
				body: JSON.stringify({ username, password })
			});
		} catch {
			return fail(503, { username, error: 'No se pudo conectar con el servidor.' });
		}

		if (response.status === 401) {
			return fail(400, { username, error: 'Usuario o contraseña incorrectos.' });
		}
		if (!response.ok) {
			return fail(502, { username, error: 'Error inesperado del servidor.' });
		}

		const { access_token } = await response.json();
		cookies.set(SESSION_COOKIE, access_token, {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: !dev,
			maxAge: 60 * 60
		});

		redirect(303, '/');
	}
};
