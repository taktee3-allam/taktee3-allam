<script lang="ts">
	import { A, Heading } from 'flowbite-svelte';
	import '../app.css';
	let { children } = $props();
</script>

<div class="flex items-center justify-between p-4">
	<A href="/" class="text-lg">
		<Heading tag="h1" class="w-fit">Text semantic splitter</Heading>
	</A>
</div>
<hr />
<main class="flex flex-row justify-evenly gap-4 p-4">
	{@render children()}
</main>
