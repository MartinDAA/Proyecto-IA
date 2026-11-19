<script lang="ts">
	import Pictograma from '#lib/components/Pictograma.svelte';
	import type { Escenario } from '#lib/juego.js';

	let {
		escenario,
		resaltar = null,
		class: className = ''
	}: { escenario: Escenario; resaltar?: string | null; class?: string } = $props();

	// Posición de cada elemento (animal, construcción, transporte, objeto) en el paisaje.
	const lugares = [
		'bottom-[6%] left-[4%]',
		'top-[6%] left-[4%]',
		'right-[4%] bottom-[6%]',
		'top-[6%] right-[4%]'
	];
</script>

<section
	class={[
		'relative aspect-[16/9] w-full overflow-hidden rounded-xl bg-linear-to-b shadow-md',
		escenario.cielo,
		className
	]}
	aria-label="Paisaje: {escenario.pictograma.nombre}"
>
	<div class="absolute inset-0 flex items-center justify-center">
		<div class="w-[34%] rounded-2xl bg-white/90 p-2 text-black shadow-lg">
			<Pictograma picto={escenario.pictograma} />
		</div>
	</div>

	{#each escenario.elementos as elemento, i (elemento.id)}
		{@const brilla = resaltar === elemento.id}
		<div
			class={[
				'absolute w-[17%] rounded-xl bg-white p-1 text-black shadow-md transition-all duration-500',
				lugares[i],
				brilla && 'z-10 scale-125 animate-pulse ring-[6px] ring-yellow-400',
				resaltar && !brilla && 'opacity-40'
			]}
		>
			<Pictograma picto={elemento} etiqueta={false} />
		</div>
	{/each}
</section>
