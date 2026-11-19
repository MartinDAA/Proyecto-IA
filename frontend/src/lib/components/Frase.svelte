<script lang="ts">
	import Pictograma from '#lib/components/Pictograma.svelte';
	import type { Mensaje } from '#lib/juego.js';

	// Frase de CAA: una fila de pictogramas que se lee de izquierda a derecha.
	let {
		mensaje,
		tamano = 'md',
		class: className = ''
	}: { mensaje: Mensaje; tamano?: 'sm' | 'md' | 'lg'; class?: string } = $props();

	const ancho = { sm: 'w-16 sm:w-20', md: 'w-14 sm:w-24', lg: 'w-20 sm:w-28' };
</script>

<div class={['flex flex-wrap items-start gap-2', className]} aria-label={mensaje.texto}>
	{#each mensaje.pictogramas as picto, i (i)}
		<div class="rounded-xl border-2 border-foreground/15 bg-white p-1 text-black {ancho[tamano]}">
			<Pictograma {picto} />
		</div>
	{/each}
</div>
