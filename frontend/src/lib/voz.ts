// Voz del juego: audios pregrabados con Piper (backend/ia_models/herramientas/generar_audios.py).
// Si un texto no tiene audio, se usa la síntesis de voz del navegador (Web Speech API).
import indice from '#lib/audio.json';

const audios: Record<string, string> = indice;

let actual: HTMLAudioElement | null = null;
let soltar: (() => void) | null = null;
// Cada llamada a hablar() invalida la secuencia anterior.
let secuencia = 0;

function vozEspanol(): SpeechSynthesisVoice | undefined {
	const voces = speechSynthesis.getVoices();
	return (
		voces.find((v) => v.lang === 'es-PE') ??
		voces.find((v) => v.lang.startsWith('es-4')) ??
		voces.find((v) => v.lang.startsWith('es'))
	);
}

function sintetizar(texto: string): Promise<void> {
	if (typeof speechSynthesis === 'undefined') return Promise.resolve();
	return new Promise((resolve) => {
		const frase = new SpeechSynthesisUtterance(texto);
		frase.lang = 'es-PE';
		frase.voice = vozEspanol() ?? null;
		frase.rate = 0.85;
		frase.pitch = 1.5;
		// Algunos navegadores no disparan "end": se usa un tiempo máximo como respaldo.
		const respaldo = setTimeout(resolve, 900 + texto.length * 90);
		const terminar = () => {
			clearTimeout(respaldo);
			resolve();
		};
		frase.onend = terminar;
		frase.onerror = terminar;
		speechSynthesis.speak(frase);
	});
}

function reproducir(archivo: string, texto: string): Promise<void> {
	return new Promise((resolve) => {
		const audio = new Audio(`/audio/${archivo}`);
		actual = audio;
		soltar = resolve;
		audio.onended = () => resolve();
		// Audio faltante: se lee con la voz del navegador.
		audio.onerror = () => sintetizar(texto).then(resolve);
		// El navegador puede bloquear el sonido hasta que el usuario toque la pantalla.
		audio.play().catch(() => resolve());
	});
}

/** Lee uno o varios textos en orden. Se resuelve al terminar (o enseguida si no hay sonido). */
export async function hablar(textos: string | string[]): Promise<void> {
	callar();
	const mia = ++secuencia;
	for (const texto of [textos].flat()) {
		if (mia !== secuencia) return;
		if (!texto) continue;
		const archivo = audios[texto];
		await (archivo ? reproducir(archivo, texto) : sintetizar(texto));
	}
}

export function callar() {
	secuencia++;
	actual?.pause();
	actual = null;
	soltar?.();
	soltar = null;
	if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel();
}

export const esperar = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
