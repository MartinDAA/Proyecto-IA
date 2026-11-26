<script lang="ts">
	import Cabecera from '#lib/components/Cabecera.svelte';
	import Pictograma from '#lib/components/Pictograma.svelte';
	import { titulo } from '#lib/juego.js';
	import type { PageProps } from './$types';

	let { data, form }: PageProps = $props();
</script>

<svelte:head>
	<title>Ajustes · K’iti Yachay</title>
</svelte:head>

<div class="flex min-h-dvh flex-col bg-background font-body">
	<Cabecera />

	<main class="mx-auto w-full max-w-5xl flex-1 px-4 py-6 sm:px-6">
		<h1 class="font-headings text-2xl font-bold">Ajustes del educador</h1>
		<p class="mt-1 text-sm text-muted-foreground">
			No se guardan datos del niño. Los ajustes se borran al cerrar el navegador.
		</p>

		<form method="POST" class="mt-6 flex flex-col gap-6">
			<fieldset class="flex flex-col gap-2">
				<legend class="mb-2 font-headings text-lg font-bold">¿Cómo ayudar tras un error?</legend>
				{#each data.perfiles as perfil (perfil.id)}
					<label class="flex items-start gap-3 rounded-xl border border-border bg-card p-4">
						<input
							type="radio"
							name="perfil"
							value={perfil.id}
							checked={perfil.id === data.ajustes.perfil}
							required
							class="mt-1 h-5 w-5"
						/>
						<span>
							<span class="block font-bold">{perfil.nombre}</span>
							<span class="text-sm">{perfil.descripcion}</span>
						</span>
					</label>
				{/each}
			</fieldset>

			<fieldset>
				<legend class="font-headings text-lg font-bold">¿Qué elementos evitar?</legend>
				<p class="mb-3 text-sm text-muted-foreground">
					No aparecerán como opción y se ocultará el paisaje al que pertenecen.
				</p>
				<div class="flex flex-col gap-3">
					{#each data.escenarios as escenario (escenario.id)}
						<div class="rounded-xl border border-border bg-card p-3">
							<h3 class="mb-2 font-bold">{titulo(escenario)}</h3>
							<div class="grid grid-cols-2 gap-2 sm:grid-cols-4">
								{#each escenario.elementos as elemento (elemento.id)}
									<label
										class="flex items-center gap-2 rounded-lg bg-white p-2 text-black has-checked:ring-4 has-checked:ring-red-600"
									>
										<input
											type="checkbox"
											name="evitar"
											value={elemento.id}
											checked={data.ajustes.evitar.includes(elemento.id)}
											class="h-5 w-5 shrink-0"
										/>
										<span class="w-12 shrink-0">
											<Pictograma picto={elemento} etiqueta={false} />
										</span>
										<span class="min-w-0 text-sm">{elemento.nombre}</span>
									</label>
								{/each}
							</div>
						</div>
					{/each}
				</div>
			</fieldset>

			{#if form?.error}
				<p class="rounded-lg bg-section-red px-3 py-2 text-sm" role="alert">{form.error}</p>
			{/if}

			<div class="flex gap-3">
				<button
					type="submit"
					class="rounded-xl bg-primary px-6 py-3 font-headings font-bold text-primary-foreground"
				>
					Guardar
				</button>
				<a href="/" class="rounded-xl border border-border px-6 py-3 font-headings font-bold">
					Cancelar
				</a>
			</div>
		</form>
	</main>
</div>
