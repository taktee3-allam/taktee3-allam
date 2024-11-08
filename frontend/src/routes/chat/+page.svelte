<script lang="ts">
	import { Button, Input, Toggle } from 'flowbite-svelte';

	type Message = { sender: 'user' | 'chatbot'; text: string };
	let messages = $state<Message[]>([]);
	let message = $state('');
	let useTaqtee3 = $state(false);
	let loading = $state(false);

	async function sendMessage() {
		if (!message.trim()) {
			return;
		}

		loading = true;
		messages.push({ sender: 'user', text: message });

		try {
			const response = await fetch('http://127.0.0.1:5000/api/prompt', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					prompt: message,
					useTaqtee3
				})
			});

			if (!response.ok) {
				throw await response.text();
			}

			const data = await response.json();
			message = '';
			messages.push({ sender: 'chatbot', text: data.response });
		} catch (error) {
			alert('Error: ' + error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="mx-auto flex h-screen max-w-7xl flex-col justify-between p-4">
	<div class="mb-4 flex-grow overflow-y-auto">
		{#each messages as { sender, text }}
			<div class="mb-2">
				<div class={sender === 'user' ? 'text-right' : 'text-left'}>
					<div
						class="inline-block rounded-lg p-2 {sender === 'user'
							? 'bg-blue-500 text-white'
							: 'bg-gray-200 text-black'}"
					>
						{text}
					</div>
				</div>
			</div>
		{/each}
	</div>
	<div class="sticky bottom-0 flex items-center space-x-2 space-x-reverse bg-white p-4">
		<Input
			bind:value={message}
			placeholder="اكتب رسالتك هنا..."
			on:keydown={(e) => e.key === 'Enter' && sendMessage()}
			disabled={loading}
			class="flex-grow"
		/>
		<Button on:click={sendMessage} disabled={loading}>أرسل</Button>
		<Toggle bind:checked={useTaqtee3} disabled={loading}>استخدم تقطيع</Toggle>
	</div>
</div>
