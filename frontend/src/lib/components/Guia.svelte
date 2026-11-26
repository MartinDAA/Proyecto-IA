<script lang="ts">
	import { onDestroy, tick } from 'svelte';
	import Frase from '#lib/components/Frase.svelte';
	import { ICONOS, POSES, type Paso } from '#lib/guia.js';
	import { callar, hablar } from '#lib/voz.js';

	// Recorrido guiado de Uku: ilumina una zona de la pantalla (como una linterna) y oscurece el resto.
	let { pasos, onterminar }: { pasos: Paso[]; onterminar: () => void } = $props();

	let i = $state(0);
	let zona = $state<DOMRect | null>(null);
	const paso = $derived(pasos[i]);
	const ultimo = $derived(i === pasos.length - 1);
	// El globo va arriba si la zona iluminada está en la mitad inferior, para no taparla.
	const arriba = $derived(zona !== null && zona.top + zona.height / 2 > innerHeight / 2);

	function objetivo() {
		return paso.objetivo ? document.querySelector(`[data-guia="${paso.objetivo}"]`) : null;
	}

	function medir() {
		zona = objetivo()?.getBoundingClientRect() ?? null;
	}

	$effect(() => {
		objetivo()?.scrollIntoView({ block: 'center' });
		tick().then(medir);
		hablar(paso.mensaje.texto);
	});
	onDestroy(callar);

	function siguiente() {
		if (ultimo) onterminar();
		else i++;
	}
</script>

<svelte:window onresize={medir} onscroll={medir} />

<!-- Capa que bloquea el juego mientras Uku explica. -->
<div class="fixed inset-0 z-40" aria-hidden="true"></div>

{#if zona}
	<div
		class="pointer-events-none fixed z-40 rounded-2xl ring-4 ring-yellow-300 motion-safe:transition-all motion-safe:duration-300"
		style:top="{zona.top - 8}px"
		style:left="{zona.left - 8}px"
		style:width="{zona.width + 16}px"
		style:height="{zona.height + 16}px"
		style:box-shadow="0 0 0 200vmax rgb(0 0 0 / 0.75)"
		aria-hidden="true"
	></div>
{:else}
	<div class="pointer-events-none fixed inset-0 z-40 bg-black/75" aria-hidden="true"></div>
{/if}

<div
	class={[
		'fixed inset-x-0 z-50 mx-auto flex max-w-3xl items-end gap-2 px-4 sm:gap-4',
		arriba ? 'top-4' : 'bottom-4'
	]}
	role="dialog"
	aria-modal="true"
	aria-label="Uku explica el juego"
>
	<img src={POSES[paso.pose]} alt="Uku" class="h-28 w-28 shrink-0 sm:h-40 sm:w-40" />
	<div class="flex min-w-0 flex-1 flex-col gap-3 rounded-2xl bg-card p-3 shadow-xl sm:p-4">
		<div class="flex items-start justify-between gap-2">
			<Frase mensaje={paso.mensaje} tamano="sm" />
			<button
				type="button"
				class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-white shadow ring-2 ring-primary"
				aria-label="Escuchar otra vez"
				onclick={() => hablar(paso.mensaje.texto)}
			>
				<img src={ICONOS.escuchar} alt="" class="h-4/5 w-4/5" />
			</button>
		</div>
		<p class="font-headings text-lg font-bold sm:text-xl" aria-live="polite">
			{paso.mensaje.texto}
		</p>
		<div class="flex items-center gap-2">
			<button
				type="button"
				class="rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-background"
				onclick={onterminar}
			>
				Saltar
			</button>
			<span class="flex-1"></span>
			{#if i > 0}
				<button
					type="button"
					class="rounded-xl border border-border px-4 py-2 font-headings font-bold hover:bg-background"
					onclick={() => i--}
				>
					←
				</button>
			{/if}
			<button
				type="button"
				class="rounded-xl bg-primary px-5 py-2 font-headings font-bold text-primary-foreground shadow-sm hover:opacity-90"
				onclick={siguiente}
			>
				{ultimo ? '¡A jugar! ▶' : 'Siguiente →'}
			</button>
		</div>
	</div>
</div>
