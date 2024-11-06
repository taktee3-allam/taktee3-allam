<script lang="ts">
	import { Heading, Button, Textarea, Label, Range, List, Li } from 'flowbite-svelte';

	let inputText = $state('');
	let threshold = $state(30);
	let loading = $state(false);
	let groupedSentences = $state<string[]>([]);

	async function submit() {
		loading = true;
		try {
			const res = await fetch('/api/split-text', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					text: inputText,
					threshold
				})
			});
			const data = await res.json();
			groupedSentences = data.groupedSentences;
		} catch (e) {
			alert('An error occured: ' + e);
		} finally {
			loading = false;
		}
	}
</script>

<Heading tag="h1" class="p-4">Text semantic splitter</Heading>
<hr />
<main class="flex flex-row justify-evenly gap-4 p-4">
	<section class="flex-1">
		<Label class="mb-2 mt-4 text-xl">Enter the text to be semantically split</Label>
		<Textarea placeholder="Text goes here..." rows={8} bind:value={inputText} disabled={loading}>
			<div slot="footer" class="flex items-center justify-between">
				<div class="w-44">
					<Label>Threshold: {threshold}%</Label>
					<Range min={0} max={100} step={1} bind:value={threshold} disabled={loading} />
				</div>
				<Button onclick={submit} disabled={loading}>Submit</Button>
			</div>
		</Textarea>
	</section>
	<section class="flex-1">
		<Heading tag="h2">Grouped sentences</Heading>
		<List class="p-2" list="decimal">
			{#each groupedSentences as sentence}
				<Li>{sentence}</Li>
			{/each}
		</List>
	</section>
</main>
