<script lang="ts">
	import type { Pictograma } from '#lib/juego.js';

	let {
		picto,
		etiqueta = true,
		class: className = ''
	}: { picto: Pictograma; etiqueta?: boolean; class?: string } = $props();

	// Si la imagen no carga se muestra el emoji equivalente.
	let fallo = $state(false);

	// Achica el nombre hasta que quepa sin partir palabras: partirlas enseña mal el vocabulario.
	function caber(nodo: HTMLElement) {
		const MINIMO = 8;
		function ajustar() {
			nodo.style.fontSize = '';
			let tamano = parseFloat(getComputedStyle(nodo).fontSize);
			while (nodo.scrollWidth > nodo.clientWidth && tamano > MINIMO) {
				nodo.style.fontSize = `${--tamano}px`;
			}
		}
		// Se observa la figura: su ancho no depende del tamaño de la letra.
		const observador = new ResizeObserver(ajustar);
		observador.observe(nodo.parentElement!);
		return { destroy: () => observador.disconnect() };
	}
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
	<!-- key: al cambiar el nombre se vuelve a ajustar el tamaño. -->
	{#key picto.nombre}
		{#if etiqueta}
			<figcaption
				use:caber
				class="w-full text-center text-xs leading-tight font-bold tracking-wide uppercase sm:text-sm"
			>
				{picto.nombre}
			</figcaption>
		{/if}
	{/key}
</figure>
