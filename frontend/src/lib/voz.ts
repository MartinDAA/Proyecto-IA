// Síntesis de voz con la Web Speech API del navegador.

function vozEspanol(): SpeechSynthesisVoice | undefined {
	const voces = speechSynthesis.getVoices();
	return (
		voces.find((v) => v.lang === 'es-PE') ??
		voces.find((v) => v.lang.startsWith('es-4')) ??
		voces.find((v) => v.lang.startsWith('es'))
	);
}

/** Lee el texto en voz alta, pausado. Se resuelve al terminar (o enseguida si no hay voz). */
export function hablar(texto: string): Promise<void> {
	if (typeof speechSynthesis === 'undefined' || !texto) return Promise.resolve();
	speechSynthesis.cancel();
	return new Promise((resolve) => {
		const frase = new SpeechSynthesisUtterance(texto);
		frase.lang = 'es-PE';
		frase.voice = vozEspanol() ?? null;
		frase.rate = 0.85;
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

export function callar() {
	if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel();
}

export const esperar = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
