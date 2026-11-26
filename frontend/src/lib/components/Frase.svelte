<script lang="ts">
	import Pictograma from '#lib/components/Pictograma.svelte';
	import type { Mensaje } from '#lib/juego.js';

	// Frase de CAA: una fila de pictogramas que se lee de izquierda a derecha.
	let {
		mensaje,
		tamano = 'md',
		class: className = ''
	}: { mensaje: Mensaje; tamano?: 'sm' | 'md' | 'lg'; class?: string } = $props();

	// Ancho de una tarjeta de palabra corta (6 letras o menos), en rem.
	const ancho = { sm: 5, md: 6, lg: 7 };
	// Por debajo de este ancho la frase pasa a la fila siguiente.
	const MINIMO = 3;

	// Las palabras largas reciben una tarjeta más ancha, pero la imagen mide lo mismo en todas.
	// Cada tarjeta parte de su ancho mínimo y crece en proporción hasta su ancho normal:
	// la frase solo pasa a otra fila cuando ni el mínimo cabe.
	function unidades(nombre: string) {
		return Math.max(6, ...nombre.split(' ').map((palabra) => palabra.length)) / 6;
	}
</script>

<div
	class={['flex w-full flex-wrap items-start gap-1.5 sm:gap-2', className]}
	aria-label={mensaje.texto}
>
	{#each mensaje.pictogramas as picto, i (i)}
		{@const u = unidades(picto.nombre)}
		<div
			class="rounded-xl border-2 border-foreground/15 bg-white p-1 text-black"
			style:flex="{u} 0 {MINIMO * u}rem"
			style:max-width="{ancho[tamano] * u}rem"
			style:--u={u}
		>
			<Pictograma
				{picto}
				class="[&>div:first-child]:mx-auto [&>div:first-child]:max-w-[calc(100%/var(--u))]"
			/>
		</div>
	{/each}
</div>
