<script lang="ts">
	import { A, Heading } from 'flowbite-svelte';
	import '../app.css';
	let { children } = $props();
</script>

<div class="flex items-center justify-between p-4">
	<A href="/" class="text-lg">
		<Heading tag="h1" class="w-fit">تقطيع الجمل حسب المعنى - تقطيع</Heading>
	</A>
	<div>
		<A href="/sentences" class="mr-4">الجمل المخزنة</A>
	</div>
</div>
<hr />
<main class="p-4">
	{@render children()}
</main>
