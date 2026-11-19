<script lang="ts">
	import { onDestroy, onMount, untrack } from 'svelte';
	import Cabecera from '#lib/components/Cabecera.svelte';
	import Escena from '#lib/components/Escena.svelte';
	import Frase from '#lib/components/Frase.svelte';
	import Pictograma from '#lib/components/Pictograma.svelte';
	import { titulo, type Mensaje, type Turno } from '#lib/juego.js';
	import { callar, esperar, hablar } from '#lib/voz.js';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	let turno = $state<Turno>(untrack(() => data.turno));
	// Opción recién elegida y si fue correcta (null mientras se espera al servidor).
	let marcado = $state<{ id: string; correcto: boolean | null } | null>(null);
	// Felicitación a pantalla completa tras un acierto.
	let felicitacion = $state<Mensaje | null>(null);
	// Retroalimentación de un error ("Pingüino no va aquí"), visible junto a la pista.
	let aviso = $state<Mensaje | null>(null);
	let ocupado = $state(false);
	let fallo = $state<string | null>(null);

	const resumen = $derived(turno.resumen);

	function decirTurno(t: Turno) {
		if (t.resumen) {
			hablar([t.resumen.frase.texto, ...t.resumen.no_pertenecen.map((m) => m.texto)].join(' '));
		} else {
			hablar(t.mensaje.texto);
		}
	}

	onMount(() => {
		decirTurno(turno);
	});
	onDestroy(callar);

	async function elegir(id: string) {
		if (ocupado || turno.terminada) return;
		ocupado = true;
		fallo = null;
		marcado = { id, correcto: null };

		let nuevo: Turno;
		try {
			const response = await fetch('/api/partida/responder', {
				method: 'POST',
				body: JSON.stringify({ partida_id: turno.partida_id, pictograma: id })
			});
			if (!response.ok) throw new Error();
			nuevo = await response.json();
		} catch {
			fallo = 'No se pudo enviar la respuesta. Inténtalo otra vez.';
			marcado = null;
			ocupado = false;
			return;
		}

		marcado = { id, correcto: nuevo.correcto };
		if (nuevo.correcto) {
			felicitacion = nuevo.retro;
			await Promise.all([hablar(nuevo.retro?.texto ?? ''), esperar(1600)]);
			felicitacion = null;
			aviso = null;
		} else {
			await esperar(700);
			aviso = nuevo.retro;
		}
		turno = nuevo;
		marcado = null;
		if (nuevo.correcto) {
			decirTurno(nuevo);
		} else {
			hablar(`${nuevo.retro?.texto ?? ''} ${nuevo.mensaje.texto}`);
		}
		ocupado = false;
	}
</script>

<svelte:head>
	<title>{titulo(turno.escenario)} · K’iti Yachay</title>
</svelte:head>

<div class="flex min-h-dvh flex-col bg-background font-body">
	<Cabecera usuario={data.user?.username} />

	{#if resumen}
		<main
			class="mx-auto flex w-full max-w-4xl flex-1 flex-col items-center gap-6 px-4 py-6 sm:py-10"
		>
			<div class="flex flex-col items-center gap-2 text-center">
				<span class="text-7xl" aria-hidden="true">{resumen.estrella ? '⭐' : '🎉'}</span>
				<h1 class="font-headings text-3xl font-bold">¡Lo lograste!</h1>
				<p class="text-muted-foreground">
					Acertaste {resumen.aciertos_primer_intento} de {turno.total_rondas} al primer intento
				</p>
			</div>

			<section class="w-full rounded-2xl bg-section-green p-4 sm:p-6">
				<div class="mb-3 flex items-center justify-between gap-2">
					<h2 class="font-headings text-lg font-bold">Esto hay en {turno.escenario.nombre}</h2>
					<button
						type="button"
						class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-card text-2xl shadow"
						aria-label="Escuchar otra vez"
						onclick={() => decirTurno(turno)}
					>
						🔊
					</button>
				</div>
				<Frase mensaje={resumen.frase} tamano="lg" />
			</section>

			{#if resumen.no_pertenecen.length}
				<section class="w-full rounded-2xl bg-section-red p-4 sm:p-6">
					<h2 class="mb-3 font-headings text-lg font-bold">Estos no van aquí</h2>
					<div class="flex flex-col gap-3">
						{#each resumen.no_pertenecen as m (m.texto)}
							<div class="flex flex-wrap items-center gap-3">
								<Frase mensaje={m} tamano="sm" />
								<span class="text-sm">{m.texto}</span>
							</div>
						{/each}
					</div>
				</section>
			{/if}

			<div class="flex flex-wrap justify-center gap-3">
				<a
					href="/"
					class="flex items-center gap-3 rounded-2xl bg-primary px-6 py-3 font-headings text-xl font-bold text-primary-foreground shadow"
				>
					<span class="w-14 rounded-lg bg-white p-1 text-black">
						<Pictograma picto={resumen.terminar} etiqueta={false} />
					</span>
					Terminar
				</a>
				<a
					href="/jugar/{turno.escenario.id}"
					data-sveltekit-reload
					class="flex items-center gap-2 rounded-2xl border border-border bg-card px-6 py-3 font-headings text-lg font-bold shadow-sm"
				>
					<span aria-hidden="true">🔁</span> Otra vez
				</a>
			</div>
		</main>
	{:else}
		<main
			class="mx-auto grid w-full max-w-6xl flex-1 content-start gap-4 px-4 py-4 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:gap-6 lg:py-6"
		>
			<div class="flex flex-col gap-3">
				<ol class="flex items-center justify-center gap-2" aria-label="Rondas">
					{#each { length: turno.total_rondas }, i (i)}
						<li
							class={[
								'flex h-9 w-9 items-center justify-center rounded-full font-bold',
								i + 1 < turno.ronda && 'bg-green-600 text-white',
								i + 1 === turno.ronda &&
									'bg-primary text-primary-foreground ring-4 ring-primary/30',
								i + 1 > turno.ronda && 'bg-dot-inactive text-foreground/60'
							]}
							aria-current={i + 1 === turno.ronda ? 'step' : undefined}
						>
							{i + 1 < turno.ronda ? '✓' : i + 1}
						</li>
					{/each}
				</ol>
				<Escena escenario={turno.escenario} resaltar={turno.resaltar} />
			</div>

			<div class="flex flex-col gap-4">
				<section class="rounded-2xl bg-card p-4 shadow-sm" aria-live="polite">
					{#if aviso}
						<div class="mb-3 flex items-center gap-3 rounded-xl bg-section-red p-2">
							<Frase mensaje={aviso} tamano="sm" />
							<span class="text-sm font-medium">{aviso.texto}</span>
						</div>
					{/if}
					<div class="flex items-start justify-between gap-3">
						<Frase mensaje={turno.mensaje} />
						<button
							type="button"
							class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-2xl text-primary-foreground shadow"
							aria-label="Escuchar otra vez"
							onclick={() => hablar(turno.mensaje.texto)}
						>
							🔊
						</button>
					</div>
					<p class="mt-2 text-sm text-muted-foreground">{turno.mensaje.texto}</p>
				</section>

				<div class="grid grid-cols-2 gap-3 sm:gap-4">
					{#each turno.opciones as opcion (opcion.id)}
						{@const elegido = marcado?.id === opcion.id}
						{@const destacado = turno.destacar === opcion.id}
						<button
							type="button"
							class={[
								'rounded-2xl border-4 bg-white p-2 text-black shadow-md transition-all duration-300 sm:p-3',
								elegido && marcado?.correcto === true && 'scale-105 border-green-600',
								elegido && marcado?.correcto === false && 'border-red-600 opacity-60',
								elegido && marcado?.correcto === null && 'border-selected-border',
								!elegido && destacado && 'animate-pulse border-yellow-400 ring-8 ring-yellow-300',
								!elegido && turno.destacar && !destacado && 'opacity-40',
								!elegido && !destacado && 'border-transparent hover:border-selected-border'
							]}
							disabled={ocupado}
							onclick={() => elegir(opcion.id)}
						>
							<Pictograma
								picto={opcion}
								class="mx-auto max-w-44 lg:max-w-32 sm:[&_figcaption]:text-base"
							/>
						</button>
					{/each}
				</div>

				{#if fallo}
					<p class="rounded-lg bg-section-red px-3 py-2 text-sm" role="alert">{fallo}</p>
				{/if}
			</div>
		</main>
	{/if}

	{#if felicitacion}
		<div
			class="fixed inset-0 z-50 flex flex-col items-center justify-center gap-4 bg-green-700/85 p-6"
			role="status"
		>
			<span class="text-8xl text-white" aria-hidden="true">✓</span>
			<Frase mensaje={felicitacion} tamano="lg" class="justify-center" />
			<p class="font-headings text-2xl font-bold text-white">{felicitacion.texto}</p>
		</div>
	{/if}
</div>
