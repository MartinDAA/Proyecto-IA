<script lang="ts">
	import type { Pictograma } from '#lib/juego.js';

	let {
		picto,
		etiqueta = true,
		class: className = ''
	}: { picto: Pictograma; etiqueta?: boolean; class?: string } = $props();

	// Sin conexión con ARASAAC se muestra el emoji equivalente.
	let fallo = $state(false);
</script>

<figure class={['flex min-w-0 flex-col items-center gap-1', className]}>
	<div
		class="flex aspect-square w-full items-center justify-center overflow-hidden rounded-lg bg-white p-[6%]"
	>
		{#if picto.imagen && !fallo}
			<img
				src={picto.imagen}
				alt={picto.nombre}
				class="h-full w-full object-contain"
				draggable="false"
				onerror={() => (fallo = true)}
			/>
		{:else}
			<span class="text-[min(4rem,10vw)] leading-none" role="img" aria-label={picto.nombre}>
				{picto.emoji}
			</span>
		{/if}
	</div>
	{#if etiqueta}
		<figcaption
			class="w-full text-center text-xs leading-tight font-bold tracking-wide [overflow-wrap:anywhere] uppercase sm:text-sm"
		>
			{picto.nombre}
		</figcaption>
	{/if}
</figure>
