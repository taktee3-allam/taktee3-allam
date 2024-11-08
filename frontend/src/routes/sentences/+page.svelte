<script lang="ts">
	import { onMount } from 'svelte';
	import {
		Input,
		Button,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { TrashBinSolid } from 'flowbite-svelte-icons';
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

	async function deleteSentence(id: number) {
		const res = confirm('هل انت متأكد؟');
		if (!res) {
			return;
		}
		const { error } = await supabase.from('sentences').delete().eq('id', id);
		if (error) {
			alert('An error occured: ' + error.message);
		} else {
			groupedSentences = groupedSentences.filter((s) => s.id !== id);
		}
	}
</script>

<Input placeholder="ابحث في الجمل" bind:value={search} class="w-full" />

<Table striped hoverable>
	<TableHead>
		<TableHeadCell class="inline-block w-7/12">الجملة</TableHeadCell>
		<TableHeadCell class="inline-block w-3/12">Embedding</TableHeadCell>
		<TableHeadCell class="inline-block w-1/12">امسح</TableHeadCell>
	</TableHead>
	<TableBody tableBodyClass="inline-block max-w-[95vw]">
		{#each filteredSentences as { id, sentence, embedding }}
			<TableBodyRow class="inline-block w-full">
				<TableBodyCell class="inline-block w-7/12 truncate">
					{sentence}
				</TableBodyCell>
				<TableBodyCell class="inline-block w-3/12 truncate">
					{embedding}
				</TableBodyCell>
				<TableBodyCell class="inline-block w-1/12 truncate">
					<Button on:click={() => deleteSentence(id)}>
						<TrashBinSolid />
					</Button>
				</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</Table>
