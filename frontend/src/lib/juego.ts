// Tipos de la API del juego (ver backend/app/models/partida.py).

export type Pictograma = {
	id: string;
	nombre: string;
	emoji: string;
	/** URL del pictograma de ARASAAC; si no carga se muestra el emoji. */
	imagen: string | null;
};

export type Escenario = {
	id: string;
	nombre: string;
	/** Clases de Tailwind del degradado (cielo → suelo). */
	cielo: string;
	pictograma: Pictograma;
	/** Un elemento por categoría: animal, construcción, transporte y objeto. */
	elementos: Pictograma[];
};

export type Mensaje = { pictogramas: Pictograma[]; texto: string };

export type Turno = {
	partida_id: string;
	escenario: Escenario;
	ronda: number;
	total_rondas: number;
	categoria: { id: string; nombre: string; pictograma: Pictograma };
	opciones: Pictograma[];
	mensaje: Mensaje;
	retro: Mensaje | null;
	elegido: string | null;
	correcto: boolean | null;
	ayuda: { accion: string; nivel: number } | null;
	resaltar: string | null;
	destacar: string | null;
	terminada: boolean;
	resumen: {
		frase: Mensaje;
		no_pertenecen: Mensaje[];
		aciertos_primer_intento: number;
		estrella: boolean;
		terminar: Pictograma;
	} | null;
};

/** "la granja" → "Granja" */
export function titulo(escenario: Escenario) {
	const nombre = escenario.pictograma.nombre;
	return nombre.charAt(0).toUpperCase() + nombre.slice(1);
}
