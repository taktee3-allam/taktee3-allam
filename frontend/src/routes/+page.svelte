<script lang="ts">
	import { Heading, Button, Textarea, Label, Range, List, Li } from 'flowbite-svelte';
	import { generateRandomColor } from '$lib/colors';
	import { supabase } from '$lib/supabase';

	type Sentence = { sentence: string; embedding: number[] };

	let inputText = $state('');
	let threshold = $state(30);
	let loading = $state(false);
	let groupedSentences = $state<Sentence[]>([]);

	async function submit() {
		loading = true;
		try {
			type GroupSentences = { grouped_sentences: Sentence[] };
			const res = await fetch('http://127.0.0.1:5000/api/split_text', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					text: inputText,
					threshold: threshold / 100
				})
			});
			const data: GroupSentences = await res.json();
			groupedSentences = data.grouped_sentences;
		} catch (e) {
			alert('An error occured: ' + e);
		} finally {
			loading = false;
		}
	}

	async function addToDB() {
		loading = true;
		try {
			const res = await supabase.from('sentences').insert(
				groupedSentences.map(({ sentence, embedding }) => ({
					sentence,
					embedding: JSON.stringify(embedding)
				}))
			);
			if (res.error) {
				throw 'An error occured: ' + res.error.message;
			}

			alert('Sentences added to database successfully');
			inputText = '';
			groupedSentences = [];
		} catch (e) {
			alert('An error occured: ' + e);
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex flex-row justify-evenly gap-4">
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
		<List class="p-2">
			{#each groupedSentences as { sentence }}
				<Li style="color: {generateRandomColor()}">{sentence}</Li>
			{/each}
		</List>
		{#if groupedSentences.length > 0}
			<Button onclick={addToDB} disabled={loading}>Add to Database</Button>
		{/if}
	</section>
</div>
