<script lang="ts">
	import { onMount } from 'svelte';
	import {
		Input,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { supabase } from '$lib/supabase';
	import type { Tables } from '$lib/database.types';

	type Sentence = Tables<'sentences'>;
	let groupedSentences = $state<Sentence[]>([]);
	let search = $state('');
	const filteredSentences = $derived(
		groupedSentences.filter((sentence) =>
			sentence.sentence.toLocaleLowerCase().includes(search.toLocaleLowerCase())
		)
	);

	onMount(async () => {
		const { data, error } = await supabase.from('sentences').select('*');
		if (error) {
			alert('An error occured: ' + error.message);
		} else {
			groupedSentences = data;
		}
	});
</script>

<Input placeholder="Search" bind:value={search} class="w-full" />

<Table striped hoverable>
	<TableHead>
		<TableHeadCell class="inline-block w-8/12">Sentence</TableHeadCell>
		<TableHeadCell class="inline-block w-3/12">Embedding</TableHeadCell>
	</TableHead>
	<TableBody tableBodyClass="inline-block max-w-[100vw]">
		{#each filteredSentences as { sentence, embedding }}
			<TableBodyRow class="inline-block w-full">
				<TableBodyCell class="inline-block w-8/12 truncate">
					{sentence}
				</TableBodyCell>
				<TableBodyCell class="inline-block w-3/12 truncate">
					{embedding}
				</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</Table>
