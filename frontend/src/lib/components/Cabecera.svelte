<script lang="ts">
	import type { Snippet } from 'svelte';
	import ThemeToggle from '#lib/components/ThemeToggle.svelte';
	import { ICONOS } from '#lib/guia.js';

	// children: controles del adulto propios de cada pantalla.
	let { children }: { children?: Snippet } = $props();

	// Los controles del adulto se abren manteniendo presionado el botón, para que el niño no los
	// active con un toque accidental.
	const ESPERA = 1000;
	let abierto = $state(false);
	let cargando = $state(false);
	let temporizador: ReturnType<typeof setTimeout> | undefined;
	let panel = $state<HTMLElement>();

	function empezar() {
		if (abierto) {
			abierto = false;
			return;
		}
		cargando = true;
		temporizador = setTimeout(() => {
			cargando = false;
			abierto = true;
		}, ESPERA);
	}

	function soltar() {
		clearTimeout(temporizador);
		cargando = false;
	}

	$effect(() => {
		if (abierto) panel?.querySelector<HTMLElement>('a, button, select')?.focus();
	});
</script>

<svelte:window
	onkeydown={(e) => {
		if (e.key === 'Escape') abierto = false;
	}}
	onpointerdown={(e) => {
		if (abierto && !(e.target as Element).closest('[data-educador]')) abierto = false;
	}}
/>

<header class="relative z-30 bg-header">
	<div class="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
		<a href="/" class="flex items-center gap-3">
			<img src={ICONOS.paisaje} alt="" class="h-10 w-10 shrink-0 rounded-lg bg-white p-0.5" />
			<span class="font-headings text-xl font-bold text-header-foreground sm:text-2xl">
				K’iti Yachay
			</span>
		</a>

		<div data-educador>
			<button
				type="button"
				class="relative overflow-hidden rounded-lg border border-white/30 px-3 py-1.5 text-sm font-medium text-header-foreground select-none hover:bg-white/15"
				aria-expanded={abierto}
				aria-controls="panel-educador"
				title="Mantén presionado un segundo"
				onpointerdown={empezar}
				onpointerup={soltar}
				onpointerleave={soltar}
				onpointercancel={soltar}
				oncontextmenu={(e) => e.preventDefault()}
				onkeydown={(e) => {
					if ((e.key === 'Enter' || e.key === ' ') && !e.repeat) {
						e.preventDefault();
						empezar();
					}
				}}
				onkeyup={soltar}
			>
				<!-- Barra que se llena mientras se mantiene presionado. -->
				<span
					class={[
						'absolute inset-y-0 left-0 bg-white/30',
						cargando ? 'w-full transition-[width] duration-1000 ease-linear' : 'w-0'
					]}
					aria-hidden="true"
				></span>
				<span class="relative">Educador</span>
			</button>

			{#if abierto}
				<div
					bind:this={panel}
					id="panel-educador"
					class="absolute top-full right-4 mt-2 flex w-64 flex-col gap-3 rounded-xl border border-border bg-card p-4 text-foreground shadow-xl sm:right-6"
					role="dialog"
					aria-label="Controles del educador"
				>
					{@render children?.()}
					<a
						href="/ajustes"
						class="rounded-lg border border-border px-3 py-2 text-center text-sm font-medium hover:bg-background"
					>
						Ajustes: perfil y elementos a evitar
					</a>
					<div class="flex items-center justify-between text-sm font-medium">
						Tema claro u oscuro
						<ThemeToggle class="border border-border hover:bg-background" />
					</div>
				</div>
			{/if}
		</div>
	</div>
</header>
