import { dev } from '$app/env';
import type { Cookies } from '@sveltejs/kit';

const COOKIE = 'ajustes';

/** Lo que elige el educador antes de jugar. No identifica al niño y se borra al cerrar el navegador. */
export type Ajustes = { perfil: string; evitar: string[] };

export function leerAjustes(cookies: Cookies): Ajustes {
	try {
		const { perfil, evitar } = JSON.parse(cookies.get(COOKIE) ?? '');
		if (typeof perfil === 'string' && Array.isArray(evitar)) return { perfil, evitar };
	} catch {
		// Sin ajustes o ilegibles: se usan los de siempre.
	}
	return { perfil: 'estandar', evitar: [] };
}

export function guardarAjustes(cookies: Cookies, ajustes: Ajustes) {
	cookies.set(COOKIE, JSON.stringify(ajustes), {
		path: '/',
		httpOnly: true,
		sameSite: 'lax',
		secure: !dev
	});
}
