<script lang="ts">
	import {
		Input,
		Button,
		Label,
		Range,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { TrashBinSolid } from 'flowbite-svelte-icons';
	import { supabase } from '$lib/supabase';
	import { onMount } from 'svelte';
	import { getEmbedding } from '$lib/api';

	type Sentence = { id: number; sentence: string; similarity: number };
	let sentences = $state<Sentence[]>([]);
	let searchText = $state('');
	let threshold = $state(30);
	let loading = $state(false);

	onMount(search);

	async function getAllSentences() {
		const { data: sentences } = await supabase.from('sentences').select('*');
		return sentences ?? [];
	}

	async function search() {
		loading = true;

		if (searchText === '') {
			sentences = (await getAllSentences()).map((s) => ({ ...s, similarity: 0 }));
			loading = false;
			return;
		}

		const embedding = await getEmbedding(searchText);
		const { data: filteredSentences } = await supabase.rpc('match_sentences', {
			query_embedding: JSON.stringify(embedding),
			match_threshold: threshold / 100,
			match_count: 10
		});

		sentences = filteredSentences ?? [];
		loading = false;
		searchText = '';
	}

	async function deleteSentence(id: number) {
		const res = confirm('هل انت متأكد؟');
		if (!res) {
			return;
		}
		const { error } = await supabase.from('sentences').delete().eq('id', id);
		if (error) {
			alert('An error occured: ' + error.message);
		} else {
			sentences = sentences.filter((s) => s.id !== id);
		}
	}
</script>

<div class="mx-auto mb-10 flex w-3/4 gap-4">
	<Input
		placeholder="ابحث في الجمل"
		bind:value={searchText}
		class="flex-grow"
		onkeydown={(e) => e.key === 'Enter' && search()}
	/>
	<div class="w-44">
		<Label>نسبة التشابه: {threshold}%</Label>
		<Range min={0} max={100} step={1} bind:value={threshold} disabled={loading} />
	</div>
	<Button onclick={search}>ابحث</Button>
</div>

<Table striped hoverable>
	<TableHead>
		<TableHeadCell class="inline-block w-9/12">الجملة</TableHeadCell>
		<TableHeadCell class="inline-block w-1/12">التشابه</TableHeadCell>
		<TableHeadCell class="inline-block w-1/12">امسح</TableHeadCell>
	</TableHead>
	<TableBody tableBodyClass="inline-block max-w-[95vw]">
		{#each sentences as { id, sentence, similarity }}
			<TableBodyRow class="inline-block w-full">
				<TableBodyCell class="inline-block w-9/12 truncate">
					{sentence}
				</TableBodyCell>
				<TableBodyCell class="inline-block w-1/12 truncate">
					{(similarity * 100).toFixed(2)}%
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
