<script lang="ts">
	import Pictograma from '#lib/components/Pictograma.svelte';
	import type { Escenario, Vista } from '#lib/juego.js';

	let {
		escenario,
		resaltar = null,
		vista = 'visibles',
		revelados = [],
		class: className = ''
	}: {
		escenario: Escenario;
		resaltar?: string | null;
		vista?: Vista;
		/** Elementos ya acertados: se ven siempre. */
		revelados?: string[];
		class?: string;
	} = $props();

	const PASOS: Vista[] = ['ocultos', 'siluetas', 'visibles'];

	// Resaltar aclara un paso el elemento buscado: de oculto a silueta, de silueta a visible.
	function vistaDe(id: string): Vista {
		if (revelados.includes(id)) return 'visibles';
		const paso = PASOS.indexOf(vista) + (resaltar === id ? 1 : 0);
		return PASOS[Math.min(paso, PASOS.length - 1)];
	}

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
	<!-- El lugar es la escena: sin marco, para que no se confunda con los elementos. -->
	<img
		src={escenario.pictograma.imagen}
		alt=""
		class="absolute top-1/2 left-1/2 h-[92%] -translate-x-1/2 -translate-y-1/2 rounded-xl object-contain"
	/>

	{#each escenario.elementos as elemento, i (elemento.id)}
		{@const brilla = resaltar === elemento.id}
		{@const como = vistaDe(elemento.id)}
		<div
			class={[
				'pegatina absolute w-[17%] rounded-xl transition-all duration-500',
				lugares[i],
				brilla && 'z-10 scale-125 animate-pulse ring-[6px] ring-yellow-400',
				resaltar && !brilla && 'opacity-40',
				como === 'siluetas' && 'silueta',
				como === 'ocultos' && 'invisible'
			]}
		>
			<Pictograma
				picto={elemento}
				etiqueta={false}
				class="[&>div:first-child]:bg-transparent [&>div:first-child]:p-0"
			/>
		</div>
	{/each}
</section>
