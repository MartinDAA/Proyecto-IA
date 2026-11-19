<script lang="ts">
	let { class: className = '' }: { class?: string } = $props();

	function toggle() {
		const dark = document.documentElement.classList.toggle('dark');
		try {
			localStorage.setItem('theme', dark ? 'dark' : 'light');
		} catch {
			// Sin almacenamiento disponible: el cambio solo dura esta visita.
		}
	}
</script>

<button
	type="button"
	class={[
		'flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-lg transition-colors',
		className
	]}
	aria-label="Cambiar entre modo claro y oscuro"
	title="Cambiar tema"
	onclick={toggle}
>
	<span class="dark:hidden" aria-hidden="true">🌙</span>
	<span class="hidden dark:inline" aria-hidden="true">☀️</span>
</button>
