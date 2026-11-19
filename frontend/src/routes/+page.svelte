<script lang="ts">
	import { untrack } from 'svelte';
	import Cabecera from '#lib/components/Cabecera.svelte';
	import Pictograma from '#lib/components/Pictograma.svelte';
	import { titulo } from '#lib/juego.js';
	import { hablar } from '#lib/voz.js';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// La pantalla principal muestra solo tres paisajes para no sobrecargar al jugador.
	const POR_PANTALLA = 3;
	let inicio = $state(untrack(() => data.inicio));
	const visibles = $derived(
		Array.from(
			{ length: POR_PANTALLA },
			(_, i) => data.escenarios[(inicio + i) % data.escenarios.length]
		)
	);
</script>

<svelte:head>
	<title>K’iti Yachay</title>
</svelte:head>

<div class="flex min-h-dvh flex-col bg-background font-body">
	<Cabecera usuario={data.user?.username} />

	<main class="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-4 py-6 sm:px-6 sm:py-10">
		<div class="flex items-center justify-center gap-3">
			<h1 class="text-center font-headings text-2xl font-bold sm:text-3xl">Elige un paisaje</h1>
			<button
				type="button"
				class="flex h-11 w-11 items-center justify-center rounded-full bg-card text-2xl shadow"
				aria-label="Escuchar"
				onclick={() => hablar('Elige un paisaje.')}
			>
				🔊
			</button>
		</div>

		<div class="grid gap-4 sm:grid-cols-3 sm:gap-6">
			{#each visibles as escenario (escenario.id)}
				<a
					href="/jugar/{escenario.id}"
					class={[
						'group flex flex-col items-center gap-3 rounded-2xl bg-linear-to-b p-5 shadow-md transition-transform hover:scale-[1.03] focus-visible:ring-4 focus-visible:ring-selected-border focus-visible:outline-none',
						escenario.cielo
					]}
					onclick={() => hablar(`Vamos a ${escenario.nombre}.`)}
				>
					<div class="w-2/3 rounded-xl bg-white p-2 text-black shadow sm:w-full">
						<Pictograma picto={escenario.pictograma} etiqueta={false} />
					</div>
					<span
						class="rounded-full bg-white px-4 py-1 font-headings text-xl font-bold text-black shadow"
					>
						{titulo(escenario)}
					</span>
				</a>
			{/each}
		</div>

		<button
			type="button"
			class="mx-auto flex items-center gap-2 rounded-xl border border-border bg-card px-5 py-3 font-headings font-bold shadow-sm hover:opacity-90"
			onclick={() => (inicio = (inicio + POR_PANTALLA) % data.escenarios.length)}
		>
			<span aria-hidden="true">🔄</span> Otros paisajes
		</button>
	</main>

	<footer class="px-4 py-3 text-center text-xs text-muted-foreground">
		Pictogramas: Sergio Palao. Origen: ARASAAC (https://arasaac.org). Licencia: CC (BY-NC-SA).
		Propiedad: Gobierno de Aragón (España).
	</footer>
</div>
