<script lang="ts">
	import type { Snippet } from 'svelte';
	import ThemeToggle from '#lib/components/ThemeToggle.svelte';

	let { usuario, children }: { usuario?: string; children?: Snippet } = $props();
</script>

<header class="bg-header">
	<div class="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
		<a href="/" class="flex items-center gap-3">
			<span
				class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-white text-xl"
				aria-hidden="true">🏞️</span
			>
			<span class="font-headings text-xl font-bold text-header-foreground sm:text-2xl">
				K’iti Yachay
			</span>
		</a>
		<div class="flex items-center gap-1 sm:gap-2">
			{@render children?.()}
			<ThemeToggle class="text-header-foreground hover:bg-white/15" />
			<form method="POST" action="/logout" class="flex items-center gap-2">
				<span class="hidden text-sm text-header-foreground opacity-90 sm:inline">{usuario}</span>
				<button
					type="submit"
					class="rounded-lg border border-white/30 px-3 py-1.5 text-sm font-medium text-header-foreground hover:bg-white/15"
				>
					Salir
				</button>
			</form>
		</div>
	</div>
</header>
