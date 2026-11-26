<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import Cabecera from '#lib/components/Cabecera.svelte';
	import Guia from '#lib/components/Guia.svelte';
	import Pictograma from '#lib/components/Pictograma.svelte';
	import Presentacion from '#lib/components/Presentacion.svelte';
	import uku from '#lib/assets/mascota/saludo.webp';
	import { GUIA_INICIO, ICONOS, primeraVez } from '#lib/guia.js';
	import { titulo } from '#lib/juego.js';
	import { hablar } from '#lib/voz.js';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// La pantalla principal muestra solo tres paisajes para no sobrecargar al jugador.
	const POR_PANTALLA = 3;
	let inicio = $state(untrack(() => data.inicio));
	const visibles = $derived(
		Array.from(
			{ length: Math.min(POR_PANTALLA, data.escenarios.length) },
			(_, i) => data.escenarios[(inicio + i) % data.escenarios.length]
		)
	);

	// Uku explica la pantalla la primera vez en la sesión; luego se puede repetir con su botón.
	let guia = $state(false);
	// Antes del juego, Uku lo presenta (una vez por sesión). null: aún no se sabe si toca mostrarla.
	let presentacion = $state<boolean | null>(null);
	onMount(() => {
		presentacion = primeraVez('presentacion');
		if (!presentacion) guia = primeraVez('guia-inicio');
	});

	function empezar() {
		presentacion = false;
		guia = primeraVez('guia-inicio');
	}
</script>

<svelte:head>
	<title>K’iti Yachay</title>
</svelte:head>

{#if presentacion}
	<Presentacion onterminar={empezar} />
{:else if presentacion === false}
	<div class="flex min-h-dvh flex-col bg-background font-body">
		<Cabecera />

		<main class="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-4 py-6 sm:px-6 sm:py-10">
			<div class="flex items-center justify-center gap-3">
				<h1 class="text-center font-headings text-2xl font-bold sm:text-3xl">Elige un paisaje</h1>
				<button
					type="button"
					data-guia="escuchar"
					class="flex h-12 w-12 items-center justify-center rounded-full bg-white shadow ring-2 ring-primary"
					aria-label="Escuchar"
					onclick={() => hablar('Elige un paisaje.')}
				>
					<img src={ICONOS.escuchar} alt="" class="h-4/5 w-4/5" />
				</button>
			</div>

			<div class="grid gap-4 sm:grid-cols-3 sm:gap-6" data-guia="paisajes">
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
				{:else}
					<p class="text-center sm:col-span-3">
						No quedan paisajes con los elementos a evitar. Cámbialos en
						<a href="/ajustes" class="font-bold underline">Ajustes</a>.
					</p>
				{/each}
			</div>

			<button
				type="button"
				data-guia="otros"
				class="mx-auto flex items-center gap-2 rounded-xl border border-border bg-card px-5 py-3 font-headings font-bold shadow-sm hover:opacity-90"
				onclick={() => (inicio = (inicio + POR_PANTALLA) % data.escenarios.length)}
			>
				<img src={ICONOS.otro} alt="" class="h-8 w-8 rounded bg-white" /> Otros paisajes
			</button>

			<button
				type="button"
				class="mx-auto flex items-center gap-2 rounded-xl px-4 py-2 font-headings font-bold hover:bg-card"
				onclick={() => (guia = true)}
			>
				<img src={uku} alt="" class="h-12 w-12" /> ¿Cómo se juega?
			</button>

			<button
				type="button"
				class="mx-auto rounded-xl px-4 py-2 font-headings font-bold hover:bg-card"
				onclick={() => (presentacion = true)}
			>
				¿De qué trata el juego?
			</button>
		</main>

		<footer class="px-4 py-3 text-center text-xs text-muted-foreground">
			Pictogramas: Sergio Palao. Origen: ARASAAC (https://arasaac.org). Licencia: CC (BY-NC-SA).
			Propiedad: Gobierno de Aragón (España).
		</footer>
	</div>
{/if}

{#if guia}
	<Guia pasos={GUIA_INICIO} onterminar={() => (guia = false)} />
{/if}
