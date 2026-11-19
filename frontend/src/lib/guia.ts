// Guía de Uku: poses de la mascota, pictogramas de sus explicaciones y pasos de cada pantalla.
import saludo from '#lib/assets/mascota/saludo.webp';
import camina from '#lib/assets/mascota/camina.webp';
import lee from '#lib/assets/mascota/lee.webp';
import animo from '#lib/assets/mascota/animo.webp';
import celebra from '#lib/assets/mascota/celebra.webp';
import type { Mensaje, Pictograma } from '#lib/juego.js';

export const POSES = { saludo, camina, lee, animo, celebra };
export type Pose = keyof typeof POSES;

export type Paso = {
	/** Valor de `data-guia` de la zona que se ilumina; sin él se oscurece toda la pantalla. */
	objetivo?: string;
	pose: Pose;
	mensaje: Mensaje;
};

function p(id: string, nombre: string, emoji: string, arasaac: number): Pictograma {
	const imagen = `https://static.arasaac.org/pictograms/${arasaac}/${arasaac}_500.png`;
	return { id, nombre, emoji, imagen };
}

// Identificadores de ARASAAC (los compartidos son los mismos de datos/escenarios.json).
const P = {
	hola: p('hola', 'hola', '👋', 6009),
	yo: p('yo', 'yo', '🙋', 2617),
	oso: p('oso', 'oso', '🐻', 2488),
	elegir: p('elegir', 'elegir', '👉', 11694),
	paisaje: p('paisaje', 'paisaje', '🏞️', 10304),
	tocar: p('tocar', 'tocar', '👆', 3293),
	aqui: p('aqui', 'aquí', '📍', 5382),
	oir: p('oir', 'escuchar', '👂', 2381),
	otro: p('otro', 'otro', '🔀', 17054),
	ayudar: p('ayudar', 'ayudar', '🤝', 4570),
	jugar: p('jugar', 'jugar', '🧸', 2439),
	mira: p('mira', 'mira', '👀', 2474),
	que: p('que', '¿qué?', '❓', 22620),
	hay: p('hay', 'hay', '👉', 10726),
	no: p('no', 'no', '🚫', 5526),
	otra_vez: p('otra_vez', 'otra vez', '🔁', 37162),
	terminar: p('terminar', 'terminar', '🏁', 5358)
};

const m = (texto: string, ...pictogramas: Pictograma[]): Mensaje => ({ texto, pictogramas });

export const GUIA_INICIO: Paso[] = [
	{ pose: 'saludo', mensaje: m('¡Hola! Yo soy Uku, el oso.', P.hola, P.yo, P.oso) },
	{ objetivo: 'paisajes', pose: 'camina', mensaje: m('Elige un paisaje.', P.elegir, P.paisaje) },
	{
		objetivo: 'escuchar',
		pose: 'lee',
		mensaje: m('Toca aquí para escuchar.', P.tocar, P.aqui, P.oir)
	},
	{
		objetivo: 'otros',
		pose: 'animo',
		mensaje: m('Toca aquí para ver otro paisaje.', P.tocar, P.aqui, P.otro, P.paisaje)
	},
	{ objetivo: 'paisajes', pose: 'celebra', mensaje: m('¡Vamos a jugar!', P.jugar) }
];

export const GUIA_JUEGO: Paso[] = [
	{ objetivo: 'paisaje', pose: 'lee', mensaje: m('Mira el paisaje.', P.mira, P.paisaje) },
	{
		objetivo: 'pregunta',
		pose: 'saludo',
		mensaje: m('Yo pregunto: ¿qué hay aquí?', P.yo, P.que, P.hay, P.aqui)
	},
	{
		objetivo: 'opciones',
		pose: 'camina',
		mensaje: m('Toca el que va en el paisaje.', P.tocar, P.paisaje)
	},
	{ pose: 'animo', mensaje: m('Si no es, yo te ayudo.', P.no, P.yo, P.ayudar) },
	{ pose: 'celebra', mensaje: m('¡Vamos a jugar!', P.jugar) }
];

export const INVITACION = m('¿Jugamos otra vez o terminamos?', P.jugar, P.otra_vez, P.terminar);

/** Devuelve true la primera vez en la sesión del navegador; sin almacenamiento, siempre true. */
export function primeraVez(clave: string): boolean {
	try {
		if (sessionStorage.getItem(clave)) return false;
		sessionStorage.setItem(clave, '1');
	} catch {
		// Almacenamiento bloqueado: se muestra la guía.
	}
	return true;
}
