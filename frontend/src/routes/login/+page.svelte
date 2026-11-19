<script lang="ts">
	import { enhance } from '$app/forms';
	import ThemeToggle from '#lib/components/ThemeToggle.svelte';
	import type { PageProps } from './$types';

	let { form }: PageProps = $props();
	let submitting = $state(false);
</script>

<svelte:head>
	<title>Ingresar · K’iti Yachay</title>
</svelte:head>

<div class="relative flex min-h-dvh items-center justify-center bg-background px-4 py-10">
	<ThemeToggle class="absolute top-4 right-4 border border-border bg-card hover:opacity-80" />

	<div class="w-full max-w-sm">
		<div class="mb-6 flex flex-col items-center gap-3 text-center">
			<div class="flex h-14 w-14 items-center justify-center rounded-xl bg-header">
				<span class="text-3xl" aria-hidden="true">🏞️</span>
			</div>
			<h1 class="font-headings text-2xl font-bold">K’iti Yachay</h1>
			<p class="text-sm text-muted-foreground">Ingreso del educador</p>
		</div>

		<form
			method="POST"
			class="flex flex-col gap-4 rounded-xl border border-border bg-card p-6 shadow-sm"
			use:enhance={() => {
				submitting = true;
				return async ({ update }) => {
					await update();
					submitting = false;
				};
			}}
		>
			<label class="flex flex-col gap-1.5 text-sm font-medium">
				Usuario
				<input
					name="username"
					autocomplete="username"
					required
					value={form?.username ?? ''}
					class="rounded-lg border border-border bg-background px-3 py-2.5 text-base outline-none focus:border-selected-border focus:ring-2 focus:ring-selected-border/30"
				/>
			</label>

			<label class="flex flex-col gap-1.5 text-sm font-medium">
				Contraseña
				<input
					name="password"
					type="password"
					autocomplete="current-password"
					required
					class="rounded-lg border border-border bg-background px-3 py-2.5 text-base outline-none focus:border-selected-border focus:ring-2 focus:ring-selected-border/30"
				/>
			</label>

			{#if form?.error}
				<p
					class="rounded-lg bg-section-red px-3 py-2 text-sm text-red-700 dark:text-red-300"
					role="alert"
				>
					{form.error}
				</p>
			{/if}

			<button
				type="submit"
				class="mt-1 rounded-xl bg-primary px-6 py-3 font-headings font-bold text-primary-foreground disabled:opacity-60"
				disabled={submitting}
			>
				{submitting ? 'Ingresando...' : 'Ingresar'}
			</button>
		</form>

		<p class="mt-4 text-center text-xs text-muted-foreground">
			Usuario de prueba: <strong>admin</strong> / <strong>admin</strong>
		</p>
	</div>
</div>
