<script lang="ts">
	import Frase from '#lib/components/Frase.svelte';
	import ThemeToggle from '#lib/components/ThemeToggle.svelte';
	import { POSES, PRESENTACION } from '#lib/guia.js';

	// Uku presenta el juego al adulto, sin audio, antes de la pantalla de paisajes.
	let { onterminar }: { onterminar: () => void } = $props();

	let i = $state(0);
	const lamina = $derived(PRESENTACION[i]);
	const ultima = $derived(i === PRESENTACION.length - 1);

	// Se piden al abrir para que no aparezcan en blanco al avanzar.
	const imagenes = new Set(
		PRESENTACION.flatMap((l) => l.mensaje.pictogramas.map((picto) => picto.imagen ?? ''))
	);

	function siguiente() {
		if (ultima) onterminar();
		else i++;
	}
</script>

<svelte:head>
	{#each imagenes as imagen (imagen)}
		<link rel="preload" as="image" href={imagen} />
	{/each}
</svelte:head>

<main class="flex min-h-dvh flex-col bg-background font-body">
	<div class="flex items-center justify-between bg-header px-4 py-3 sm:px-6">
		<span class="font-headings text-xl font-bold text-header-foreground sm:text-2xl">
			K’iti Yachay
		</span>
		<ThemeToggle class="text-header-foreground hover:bg-white/15" />
	</div>

	<div
		class="mx-auto flex w-full max-w-5xl flex-1 flex-col items-center justify-center gap-4 px-4 py-6 sm:flex-row sm:gap-8 sm:px-6"
	>
		<img
			src={POSES[lamina.pose]}
			alt="Uku, el oso"
			width="460"
			height="460"
			class="h-44 w-44 shrink-0 sm:h-72 sm:w-72 lg:h-96 lg:w-96"
		/>

		<div
			class="flex w-full min-w-0 flex-1 flex-col gap-4 rounded-2xl bg-card p-5 shadow-md sm:min-h-104 sm:p-8"
		>
			<div class="flex flex-col gap-4" aria-live="polite">
				<h1 class="font-headings text-2xl font-bold sm:text-4xl">{lamina.titulo}</h1>
				<p class="text-lg leading-relaxed sm:text-xl">{lamina.mensaje.texto}</p>
			</div>
			<!-- key: sin él, el pictograma anterior queda a la vista mientras carga el nuevo. -->
			{#key i}
				<div aria-hidden="true">
					<Frase mensaje={lamina.mensaje} tamano="lg" />
				</div>
			{/key}

			<div class="mt-auto flex flex-wrap items-center justify-between gap-3 pt-2">
				<button
					type="button"
					class="rounded-xl px-3 py-3 font-medium hover:bg-background"
					onclick={onterminar}
				>
					Saltar
				</button>
				<span class="text-sm font-medium">{i + 1} de {PRESENTACION.length}</span>
				<div class="flex gap-2">
					<button
						type="button"
						class="rounded-xl border border-border px-5 py-3 font-headings font-bold hover:bg-background disabled:opacity-40"
						aria-label="Anterior"
						disabled={i === 0}
						onclick={() => i--}
					>
						←
					</button>
					<button
						type="button"
						class="rounded-xl bg-primary px-6 py-3 font-headings font-bold text-primary-foreground shadow-sm hover:opacity-90"
						onclick={siguiente}
					>
						{ultima ? 'Empezar ▶' : 'Siguiente →'}
					</button>
				</div>
			</div>
		</div>
	</div>
</main>
